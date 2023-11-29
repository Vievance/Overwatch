from app import db
import datetime


class User(db.Model):
    """User model for authentication and identification"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.Unicode(32))
    surname = db.Column(db.Unicode(32))
    username = db.Column(db.String(128), unique=True)

    @property
    def name(self):
        # display full name of user
        return self.forename + " " + self.surname

    def create_goal(self, text):
        # check some text has been entered
        if not text.strip():
            raise ValueError("Goals must have some text")

        goal = Goal(text=text)
        self.goals.append(goal)
        return goal


class Goal(db.Model):
    """Big overall goals for individual users, comprising of actions"""

    __tablename__ = "goal"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    completed = db.Column(db.DateTime)
    percentage_complete = db.Column(db.SmallInteger, default=0)
    text = db.Column(db.Unicode(512), nullable=False)
    
    user = db.relationship(
        "User",
        backref=db.backref(
            "goals",
            order_by="Goal.created",
            cascade="all,delete-orphan",
            lazy="dynamic",
        ),
    )

    def create_action(self, text):
        # check some text has been entered
        if not text.strip():
            raise ValueError("Actions must have some text")

        action = GoalAction(text=text)
        self.actions.append(action)

        db.session.flush()  # in case refresh_percentage_complete uses further queries

        self.refresh_percentage_complete()

        return action

    def mark_as_complete(self):
        self.completed = datetime.datetime.utcnow()

    @property
    def base_actions(self):
        # fetch non-nested actions
        return self.actions.filter(GoalAction.parent_action_id == None)
    
    @property
    def youngest_children(self):
        return self.actions.filter(GoalAction.child_actions == None)

    # TODO - 2
    def refresh_percentage_complete(self):
        completed = 0
        for action in self.youngest_children:
            if action.completed != None:
                completed += action.get_share()
        self.percentage_complete = int(completed*100)
        print(self.percentage_complete)
        return self.percentage_complete

    def delete_goal(self):
        db.session.delete(self)


class GoalAction(db.Model):
    """Actions & nested sub-actions for goals"""

    __tablename__ = "goalaction"

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=False)
    parent_action_id = db.Column(db.Integer, db.ForeignKey("goalaction.id"))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    completed = db.Column(db.DateTime)
    text = db.Column(db.Unicode(512), nullable=False)

    goal = db.relationship(
        "Goal",
        backref=db.backref(
            "actions",
            order_by="GoalAction.created",
            cascade="all,delete-orphan",
            lazy="dynamic",
        ),
    )
    parent_action = db.relationship(
        "GoalAction",
        remote_side="GoalAction.id",
        foreign_keys="GoalAction.parent_action_id",
        backref=db.backref(
            "child_actions",
            remote_side="GoalAction.parent_action_id",
            cascade="all,delete-orphan",
            order_by="GoalAction.created",
        ),
    )

    def get_youngest_children(self):
        return self.child_actions.filter(GoalAction.child_actions == None).all()


#Updates the completion of parent actions recursively
    def refresh_parent_action(self, parent=None):
        if parent is None:
            parent = self.parent_action

        if parent:
            if isinstance(parent, Goal):
                pass
            elif isinstance(parent, GoalAction):
                x = 0
                for child in parent.child_actions:
                    if child.completed == None:
                        x +=1
                if x == 0:
                    parent.completed = datetime.datetime.utcnow()
                else:
                    parent.completed = None

                # Check to see if another parent to refresh
                if parent.parent_action_id == None:
                    pass
                else:
                    self.refresh_parent_action(parent.parent_action)
        self.goal.refresh_percentage_complete()

    def create_subaction(self, text):
        # check some text has been entered
        if not text.strip():
            raise ValueError("Actions must have some text")

        if self.completed:
            self.completed = None

        action = GoalAction(text=text, goal=self.goal)
        db.session.add(action)

        self.child_actions.append(action)
        db.session.flush()  # in case refresh_percentage_complete uses further queries
        self.goal.refresh_percentage_complete()
        return action


    def mark_as_complete(self):
        children = self.child_actions
        if children:
            for child in children:
                if child.completed is None:
                    raise ValueError("Must complete all sub-actions first")
        self.completed = datetime.datetime.utcnow()
        self.refresh_parent_action()

    # TODO - 1
    def unmark_as_complete(self):
        self.completed = None
        self.refresh_parent_action()
        

    def delete_action(self):
        goal = self.goal
        self.goal.actions.remove(self)
        db.session.flush()  # in case refresh_percentage_complete uses further queries
        goal.refresh_percentage_complete()

    def get_share(self,share=None):
        if share is None:
            share = 1
        if self.parent_action:
            share *= 1/len(self.parent_action.child_actions)
            share = self.parent_action.get_share(share)
        else:
            share *= 1/len(self.goal.base_actions.all())
        return share
    
