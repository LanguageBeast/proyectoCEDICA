document.addEventListener('DOMContentLoaded', function() {
    const filterRadios = document.querySelectorAll('.filter-radio');
    const searchInput = document.getElementById('searchInput');
    const jobPositionSelect = document.getElementById('job_position');

    filterRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'job_position') {
                // Si se selecciona 'Puesto laboral'
                searchInput.style.display = 'none'; // Ocultar el input de búsqueda
                searchInput.disabled=true;
                jobPositionSelect.style.display = 'block'; // Mostrar la lista de puestos
                jobPositionSelect.disabled = false; // Habilitar la lista de puestos
            } else {
                // Si se selecciona cualquier otro filtro
                searchInput.disabled=false;
                searchInput.style.display = 'block'; // Mostrar el input de búsqueda
                jobPositionSelect.style.display = 'none'; // Ocultar la lista de puestos
                jobPositionSelect.disabled = true; // Deshabilitar la lista de puestos
                jobPositionSelect.selectedIndex = 0; // Resetear la selección
            }
        });
    });
});