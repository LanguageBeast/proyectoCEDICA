<template>
  <div class="container p-5">
    <div class="d-flex justify-content-center align-items-center">
      <div class="container-fluid p-0">
        <div class="row justify-content-center">
          <div class="col-12 col-lg-6">
            <h1>Contacto</h1>
            <p>Envíanos un mensaje y te responderemos lo antes posible.</p>
            <form @submit.prevent="submitForm">
              <div class="form-group mb-3">
                <label class="form-control-label" for="full_name">Nombre completo</label>
                <input
                  class="form-control"
                  id="full_name"
                  v-model="form.full_name"
                  type="text"
                  :class="{ invalid: errors.full_name }"
                  required
                />
                <p v-if="errors.full_name" class="error">{{ errors.full_name }}</p>
              </div>

              <div class="form-group mb-3">
                <label class="form-control-label" for="email">Correo electrónico</label>
                <input
                  class="form-control"
                  id="email"
                  v-model="form.email"
                  type="email"
                  :class="{ invalid: errors.email }"
                  required
                />
                <p v-if="errors.email" class="error">{{ errors.email }}</p>
              </div>

              <div class="form-group mb-3">
                <label class="form-control-label" for="message">Mensaje</label>
                <textarea
                  class="form-control"
                  id="message"
                  v-model="form.message"
                  :class="{ invalid: errors.message }"
                  required
                ></textarea>
                <p v-if="errors.message" class="error">{{ errors.message }}</p>
              </div>

              <div class="form-group mb-3">
                <p class="m-0" for="captcha">Escribe el texto que ves en la siguiente imagen:</p>
                <img
                  alt=""
                  class="mt-1 mb-2"
                  src="@/assets/images/captcha_pic.jpeg"
                  width="250"
                  height="50"
                />
                <input
                  class="form-control"
                  id="captcha"
                  v-model="form.captcha"
                  type="text"
                  :class="{ invalid: errors.captcha }"
                  required
                />
                <p v-if="errors.captcha" class="error">{{ errors.captcha }}</p>
              </div>
              <div class="form-group mb-3">
                <button class="btn btn btn-primary" type="submit">Enviar</button>
              </div>
              <p v-if="successMessage" class="success">{{ successMessage }}</p>
              <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            </form>
            <!-- <img alt="" class="mt-1 mb-2" src="@/assets/images/LogoCedica.jpg"/> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  full_name: 'ContactComp',
  data() {
    return {
      form: {
        full_name: '',
        email: '',
        message: '',
        captcha: '',
      },
      errors: {
        full_name: null,
        email: null,
        message: null,
        captcha: null,
      },
      successMessage: null,
      errorMessage: null,
    }
  },
  methods: {
    validateForm() {
      this.errors = { full_name: null, email: null, message: null, captcha: null }

      if (!this.form.full_name) {
        this.errors.full_name = 'El nombre completo es obligatorio.'
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!this.form.email || !emailRegex.test(this.form.email)) {
        this.errors.email = 'Ingresa una dirección de correo electrónico válida.'
      }

      if (!this.form.message) {
        this.errors.message = 'El mensaje es obligatorio.'
      }

      if (this.form.captcha !== 'equinoterapia') {
        this.errors.captcha = 'Captcha incorrecto.'
      }

      return Object.values(this.errors).every((error) => !error)
    },
    async submitForm() {
      if (!this.validateForm()) {
        return
      }

      try {
        const response = await axios.post(
          'https://admin-grupo07.proyecto2024.linti.unlp.edu.ar/api/consultant/',
          {
            full_name: this.form.full_name,
            email: this.form.email,
            message: this.form.message,
            captcha: this.form.captcha,
          },
        )

        if (response.status === 200) {
          this.successMessage = '¡Mensaje enviado exitosamente!'
          this.form = { name: '', email: '', message: '', captcha: '' }
        }
      } catch (error) {
        this.errorMessage = 'Error al enviar el mensaje. Inténtalo nuevamente.'
      }
    },
  },
}
</script>

<style scoped>
.error {
  color: red;
  font-size: 1.3em;
}

.success {
  color: green;
  font-size: 1.3em;
}

.invalid {
  border: 1px solid red;
}

form div {
  margin-bottom: 1rem;
}
</style>
