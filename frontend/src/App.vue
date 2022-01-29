<template>
<div>
  <NavBar/>
  <router-view/>
</div>
</template>

<script>
  import NavBar from "./components/NavBar.vue"
  export default {
    name: "App",
    components: {
    NavBar,
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
  }
  .main-box {
      margin: auto;
      margin-top: 60px;
      width: 50%;
      }
</style>
