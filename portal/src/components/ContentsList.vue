<template>
  <div class="container mt-5">
    <!-- Título del módulo -->
    <div class="text-center mb-4">
      <h1 class="display-4 fw-bold text-secondary">Portal de Contenidos</h1>
      <p class="lead text-secondary">Visualiza los artículos publicados de CEDICA</p>
    </div>

    <div class="row g-2 mb-4">
      <div class="col-12 col-md-3">
        <label for="startDate" class="form-label">Fecha de inicio</label>
        <input type="date" id="startDate" v-model="startDate" class="form-control" />
      </div>
      <div class="col-12 col-md-3">
        <label for="endDate" class="form-label">Fecha de fin</label>
        <input type="date" id="endDate" v-model="endDate" class="form-control" />
      </div>
      <div class="col-12 col-md-3">
        <label for="author" class="form-label">Autor</label>
        <input
          type="text"
          id="author"
          v-model="author"
          placeholder="Nombre del autor"
          class="form-control"
        />
      </div>
      <div class="col-12 col-md-3 d-flex align-items-end">
        <button class="btn btn-secondary fw-bold px-4 py-2 shadow-sm w-100" @click="applyFilters">
          <i class="bi bi-funnel-fill me-2"></i>Filtrar
        </button>
      </div>
    </div>

    <!-- Indicador de carga -->
    <div v-if="isLoading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <!-- Mensaje de error -->
    <div v-if="hasError" class="alert alert-danger" role="alert">
      {{ hasError }}
    </div>

    <!-- Lista de contenidos -->
    <div class="row" v-if="!isLoading && !hasError && allContents.length > 0">
      <div class="col-md-4 mb-4" v-for="content in allContents" :key="content.id">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <!-- Fecha de publicación -->
            <p class="card-text text-muted mb-1">
              <small>{{ formatDate(content.created_at) }}</small>
            </p>

            <!-- Título -->
            <h5 class="card-title text-primary">{{ content.title }}</h5>

            <!-- Copete -->
            <p class="card-text text-muted">
              {{ content.summary }}
            </p>

            <button class="btn btn-outline-primary w-100" @click="redirectToDetails(content.id)">
              Ver más
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Mensaje si no hay contenidos -->
    <div v-if="!isLoading && !hasError && allContents.length === 0" class="text-center">
      <p class="text-muted">No hay contenidos disponibles en este momento.</p>
    </div>

    <!-- Paginación -->
    <div v-if="!isLoading && !hasError && Pages >= 1" class="d-flex justify-content-center">
      <div class="d-flex p-2 bd-highlight">
        <ul class="pagination">
          <li class="active mx-2">
            <button class="btn btn-secondary" :disabled="Page === 1" @click="goToPreviousPage">
              Anterior
            </button>
          </li>
          <span class="mx-2">Página {{ Page }} de {{ Pages }}</span>
          <li class="active mx-2">
            <button class="btn btn-secondary" :disabled="Page === Pages" @click="goToNextPage">
              Siguiente
            </button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { useContentStore } from '@/stores/contents'
import { storeToRefs } from 'pinia'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'ContentList',
  setup() {
    const contentStore = useContentStore()
    const { fetchContents, setPage, setFilters } = contentStore

    const { allContents, isLoading, hasError, Page, Pages } = storeToRefs(contentStore)
    const router = useRouter()

    const startDate = ref('')
    const endDate = ref('')
    const author = ref('')

    const applyFilters = () => {
      setFilters(startDate.value, endDate.value, author.value)
      setPage(1) // Resetear a la primera página
      fetchContents()
    }
    const goToNextPage = () => {
      const newPage = Page.value + 1
      setPage(newPage) // Actualiza el número de página
      fetchContents(newPage) // Realiza la consulta con la nueva página
    }
    const goToPreviousPage = () => {
      const newPage = Page.value - 1
      setPage(newPage) // Actualiza el número de página
      fetchContents(newPage) // Realiza la consulta con la nueva página
    }

    const redirectToDetails = (id) => {
      router.push(`/content/${id}`)
    }

    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric' }
      return new Date(dateString).toLocaleDateString('es-ES', options)
    }

    onMounted(() => {
      fetchContents()
    })

    return {
      allContents,
      isLoading,
      hasError,
      Page,
      Pages,
      startDate,
      endDate,
      author,
      formatDate,
      redirectToDetails,
      applyFilters,
      goToPreviousPage,
      goToNextPage,
      setPage,
    }
  },
}
</script>

<style scoped>
/* Espaciado y estilo de las tarjetas */
.card {
  transition: transform 0.2s;
  border: 1px solid #ddd;
}

.card:hover {
  transform: scale(1.03);
}

/* Títulos */
h1 {
  color: black;
}

/* Botón */
.btn {
  font-weight: bold;
}

/* Contenedor principal */
.container {
  max-width: 1200px;
}

.pagination {
  display: flex;
  padding-left: 0;
  margin: 20px 0;
  border-radius: 4px;
}
.pagination > li:first-child > button,
.pagination > li:first-child > span {
  margin-left: 0;
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}
.pagination > .disabled > button,
.pagination > .disabled > button:focus,
.pagination > .disabled > button:hover,
.pagination > .disabled > span,
.pagination > .disabled > span:focus,
.pagination > .disabled > span:hover {
  color: #777;
  cursor: not-allowed;
  background-color: #fff;
  border-color: #ddd;
}
.pagination > li > button,
.pagination > li > span {
  position: relative;
  float: left;
  padding: 6px 12px;
  margin-left: -1px;
  line-height: 1.42857143;
  color: #337ab7;
  text-decoration: none;
  background-color: #fff;
  border: 1px solid #ddd;
}
.pagination > li > button:hover,
.pagination > li > span:hover {
  z-index: 2;
  color: #23527c;
  background-color: #eee;
  border-color: #ddd;
}
</style>
