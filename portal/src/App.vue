<template>
  <div id="app">
    <!-- Navbar global -->
    <header>
      <Navbar />
    </header>

    <!-- Contenido principal -->
    <main>
      <router-view />
    </main>

    <!-- Footer global -->
    <footer>
      <Footer />
    </footer>
  </div>
</template>

<script>
// Importar los componentes globales
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer,
  },
}
</script>

<style>
/* Hacer que el contenedor principal use toda la altura de la ventana */
html,
body {
  height: 100%; /* Altura completa */
  margin: 0; /* Quitar márgenes por defecto */
}

#app {
  display: flex; /* Usar Flexbox */
  flex-direction: column; /* Organizar en columna */
  min-height: 100vh; /* Asegurar que use toda la altura de la ventana */
}

header {
  background: linear-gradient(30deg, rgb(67, 180, 245), rgb(246, 193, 17), rgb(67, 180, 245));
  padding: 10px 0;
  border-bottom: 1px solid #757575;
}

main {
  flex: 1; /* Hacer que el contenido principal ocupe el espacio disponible */
}
</style>
