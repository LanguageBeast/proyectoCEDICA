import { defineStore } from 'pinia'
import axios from 'axios'

export const useContentStore = defineStore('ContentStore', {
  state: () => ({
    contents: [],
    loading: false,
    error: null,
    currentPage: 1,
    per_page: 3,
    startDate: null,
    endDate: null,
    author: null,
    totalPages: 1,
  }),

  getters: {
    allContents: (state) => state.contents,
    isLoading: (state) => state.loading,
    hasError: (state) => state.error,
    Page: (state) => state.currentPage,
    Pages: (state) => state.totalPages,
  },

  actions: {
    async fetchContents() {
      this.loading = true
      this.error = null

      try {
        // Preparar parámetros de consulta para la API
        const params = {
          page: this.currentPage,
          per_page: this.per_page,
          start_date: this.startDate,
          end_date: this.endDate,
          author: this.author,
        }

        // Realizar la solicitud a la API
        const response = await axios.get('https://admin-grupo07.proyecto2024.linti.unlp.edu.ar/api/module_content/', { params })
        const { data, page, total, per_page } = response.data

        // Actualizar el estado con los datos recibidos
        this.contents = data
        this.currentPage = page
        this.per_page = per_page
        this.totalPages = Math.floor((total + per_page - 1) / per_page)
      } catch (error) {
        if (error.response) {
          // La solicitud fue hecha y el servidor respondió con un código de estado fuera del rango 2xx
          this.error = error.response.data.error || 'Error inesperado del servidor'
          console.error(`Error ${error.response.status}: ${this.error}`)
        } else if (error.request) {
          // La solicitud fue hecha pero no hubo respuesta
          this.error = 'No se pudo conectar con el servidor.'
          console.error('No response received:', error.request)
        } else {
          // Algo pasó al configurar la solicitud
          this.error = 'Error al configurar la solicitud.'
          console.error('Request error:', error.message)
        }
      } finally {
        // Detener el indicador de carga
        this.loading = false
      }
    },

    setFilters(startDate, endDate, author) {
      this.startDate = startDate
      this.endDate = endDate
      this.author = author
    },

    setPage(page) {
      this.currentPage = page
    },
  },
})
