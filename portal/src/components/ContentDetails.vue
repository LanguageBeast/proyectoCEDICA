<template>
  <div class="container mt-5">
    <!-- Título del contenido -->
    <div class="text-center mb-4">
      <h1 class="display-4 fw-bold text-secondary">{{ content.title }}</h1>
      <p class="text-muted">Publicado el: {{ formatDate(content.created_at) }}</p>
    </div>

    <!-- Información principal del contenido -->
    <div class="card shadow-lg border-0 mb-5">
      <div class="card-body">
        <p><strong>Autor:</strong> {{ content.author_alias }}</p>
        <p>
          <strong>Estado: </strong>
          <span>
            {{ content.status }}
          </span>
        </p>
        <p v-if="content.updated_at">
          <strong>Fecha de Modificación:</strong> {{ formatDate(content.updated_at) }}
        </p>
        <p class="mt-4 text-justify">{{ content.content }}</p>
      </div>
    </div>

    <!-- Botón volver -->
    <div class="d-flex justify-content-center mt-4">
      <router-link to="/contenidos" class="btn btn-secondary px-4 py-2"> Volver </router-link>
    </div>
  </div>
</template>

<script>
import { useContentStore } from '@/stores/contents'
import { storeToRefs } from 'pinia'

export default {
  name: 'ContentDetails',
  props: ['id'],
  setup(props) {
    const contentStore = useContentStore()
    const { contents } = storeToRefs(contentStore)

    // Encontrar el contenido específico
    const content = contents.value.find((c) => c.id === parseInt(props.id))

    // Formatear fecha
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric' }
      return new Date(dateString).toLocaleDateString('es-ES', options)
    }
    return { content, formatDate }
  },
}
</script>

<style scoped>
.container {
  max-width: 800px;
  padding-bottom: 3rem; /* Espacio adicional para evitar estar pegado al footer */
}

/* Tarjeta */
.card {
  background-color: #f9f9f9;
  border-radius: 10px;
}

/* Texto justificado */
.text-justify {
  text-align: justify;
}

/* Espaciado del botón */
.btn {
  font-weight: bold;
  margin-top: 20px;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
