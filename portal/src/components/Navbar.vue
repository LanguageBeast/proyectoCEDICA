<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <!-- Enlace a la página de inicio con el logo -->
      <router-link class="navbar-brand" to="/">
        <img
          src="@/assets/images/LogoCedica.jpg"
          alt="Logo Cedica"
          width="80"
          height="30"
          class="ms-3 me-3"
        />
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
        @click="toggleNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Cambiar clase 'collapse' según el estado -->
      <div class="navbar-collapse" :class="{ collapse: !isNavbarOpen }" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.path === '/' }" to="/"
              >Home</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              :class="{
                active: $route.path === '/contenidos' || $route.path.startsWith('/content/'),
              }"
              to="/contenidos"
              >Contenidos</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              :class="{ active: $route.path === '/mensajes' }"
              to="/mensajes"
              >Mensajes</router-link
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      isNavbarOpen: false, // Estado del menú (abierto o cerrado)
    }
  },
  methods: {
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen // Alterna entre abierto/cerrado
    },
  },
}
</script>

<style scoped>
/* Opcional: añade animaciones para que el colapso sea más fluido */
.navbar-collapse.collapse {
  display: none; /* Oculta el menú cuando está colapsado */
}

.navbar-collapse {
  display: block; /* Asegura que se muestre el menú cuando no está colapsado */
}

@media (max-width: 992px) {
  .navbar-collapse {
    transition: all 0.3s ease-in-out; /* Animación suave */
  }
}
</style>
