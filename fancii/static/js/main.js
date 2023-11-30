function deleteHero(heroId) {
    fetch(`/heroes/delete/${heroId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        document.querySelector(`.hero${heroId}Container`).style.display = 'none';
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('Failed to delete hero. Please try again.');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const loadFormButton = document.getElementById('new_hero_button');
    const formContainter = document.getElementById('new_hero_container');

    loadFormButton.addEventListener('click', async () => {
        console.log('click');
        
        try {
            const response = await fetch('/heroes/get_form', {
                method: 'GET',
                headers: {
                    'Content-Type': 'text/html',
                },
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch form');
            }
            
            const formHtml = await response.text();
            formContainter.innerHTML = formHtml;

            const heroForm = document.getElementById('heroForm');
            heroForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                await submitForm(heroForm);
            });

        } catch (error) {
                console.error('Error fetching form:', error);
            
        }
    });

    async function submitForm(form) {
        const formData = new FormData(form)

        try {
            const response = await fetch('/heroes/create_hero', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new error('Failed to create hero');
            }

            const responseData = await response.json();
            console.log(responseData);
            location.reload();

        } catch (error) {
            console.error('Error creating hero:', error);
        }
    }
});
