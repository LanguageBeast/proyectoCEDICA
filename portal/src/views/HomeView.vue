<template>
  <div class="d-flex justify-content-center align-items-center">
    <div class="container-fluid text-center">
      <div class="row justify-content-center">
        <div class="col-12 col-sm-10 col-md-8 col-lg-6">
          <div class="container mt-4 mt-md-5 text-box">
            <h2 class="title">
              Centro de Equitación para Personas con Discapacidad y Carenciadas CEDICA
            </h2>
            <p class="text">
              CEDICA es una Asociación Civil sin Fines de Lucro, fundada en 1994 en la ciudad de La
              Plata, Provincia de Buenos Aires, Argentina. CEDICA trabaja con la finalidad de
              IGUALAR OPORTUNIDADES en procura de la reinserción familiar, el logro de la
              escolaridad, la integración laboral y la mejora integral de la calidad de vida de los
              J&A (“Jinetes” y “Amazonas”) que forman parte de la institución.
            </p>
            <p class="text">
              Las actividades que se realizan se denominan Terapias y Actividades asistidas con
              Caballos –TACAs-, aunque históricamente también fueron conocidas con otros términos
              como Rehabilitación Ecuestre o Equinoterapia. Se trata de una terapia integral que
              apunta a la recuperación de la persona en sus dimensiones biológica, psíquica y
              social. El principal recurso de trabajo es el Caballo, como mediador y facilitador de
              las intervenciones terapéuticas que cada profesional de la salud o la educación
              planifica para las diferentes Personas con Discapacidad que asisten a la institución.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
}
</script>

<style scoped>
.title {
  font-size: 2.5rem; /* Tamaño grande para destacar */
  font-weight: bold; /* Hacer el título en negrita */
  color: #333333; /* Color personalizado */
}

.text {
  font-size: 1.1rem; /* Ajuste del tamaño de la fuente */
  line-height: 1.6; /* Mejorar el espaciado entre líneas para legibilidad */
  color: #666666; /* Un color gris suave */
}

.text-box {
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  margin-top: 5rem;
  margin-bottom: 5rem;
  padding: 1.5rem; /* Espaciado interno para el contenido */
  max-width: 100%; /* Limitar el tamaño máximo del cuadro */
}

@media (max-width: 576px) {
  .title {
    font-size: 1.8rem; /* Reducir el tamaño de la fuente en pantallas pequeñas */
  }

  .text {
    font-size: 1rem; /* Ajustar la fuente para mejorar la legibilidad */
  }

  .text-box {
    padding: 1rem; /* Reducir el espaciado interno */
    margin-top: 3rem; /* Reducir márgenes en pantallas pequeñas */
  }
}
</style>
