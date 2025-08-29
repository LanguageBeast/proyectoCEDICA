document.addEventListener('DOMContentLoaded', function() {
    const filterRadios = document.querySelectorAll('.filter-radio');
    const searchInput = document.getElementById('searchInput');
    const paymentTypeSelect = document.getElementById('payment_type_s');
    const startDate = document.getElementById('start_date_s');
    const endDate = document.getElementById('end_date_s');
    const searchButton = document.getElementById('search_button');

    filterRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'payment_date') {
                searchInput.style.display = 'none';
                startDate.style.display = 'block';
                endDate.style.display = 'block';
                paymentTypeSelect.style.display = 'none';
                paymentTypeSelect.selectedIndex = 0;
                searchButton.style.display = 'block';
                // Hacer obligatorios los campos de fecha y quitar required del desplegable
                startDate.querySelector('input').required = true;
                endDate.querySelector('input').required = true;
                paymentTypeSelect.required = false;

            } else if (this.value === 'payment_type') {
                searchInput.style.display = 'none';
                startDate.style.display = 'none';
                endDate.style.display = 'none';
                paymentTypeSelect.style.display = 'block';
                searchButton.style.display = 'block';
                // Hacer obligatorio el desplegable y quitar required de los campos de fecha
                startDate.querySelector('input').required = false;
                endDate.querySelector('input').required = false;
                paymentTypeSelect.required = true;

            } else {
                // Si no selecciona ningún filtro
                searchInput.style.display = 'block';
                paymentTypeSelect.style.display = 'none';
                paymentTypeSelect.selectedIndex = 0;
                startDate.style.display = 'none';
                endDate.style.display = 'none';
                searchButton.style.display = 'none';
                // Deshabilitar la validación requerida para todos los campos
                startDate.querySelector('input').required = false;
                endDate.querySelector('input').required = false;
                paymentTypeSelect.required = false;
            }
        });
    });
});