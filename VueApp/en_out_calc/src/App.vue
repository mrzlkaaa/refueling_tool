<template>
  <div>
    <h1> Add new weekly Data </h1>
    <div class="card text-center">
        <div class="card-header">
              Calculate Thermal Power Output
        </div>
        <div class="card-body">
              
              <Container></Container>
              <br>
              
        </div>
    </div>
  </div>
</template>

<script>
import Container from "./components/Container.vue"

export default {
  name: 'App',
  components: {
    Container,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}
.main-box {
    margin: 0 auto;
    width: 50%;
}
.table {
    text-align: center;
}
</style>
