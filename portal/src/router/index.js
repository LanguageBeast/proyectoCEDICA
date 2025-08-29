import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ContentsView from '@/views/ContentsView.vue'
import ContactView from '@/views/ContactView.vue'
import ContentDetails from '@/components/ContentDetails.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/contenidos',
      name: 'contenidos',
      component: ContentsView,
    },
    {
      path: '/mensajes',
      name: 'mensajes',
      component: ContactView,
    },
    { path: '/content/:id', component: ContentDetails, props: true },
  ],
})

export default router
