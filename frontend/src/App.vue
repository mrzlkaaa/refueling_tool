<template>
<div style="position:relative">
  <NavBar
  v-if="isAccess()"
  />
  <Modal/>
  <AlertBox/>
  <i v-if="isAccess()" class="fa-solid fa-circle-question fa-2xl" @click="showForm"></i>
  <router-view/>
  <Report
    v-if="isAccess() && isDisplayed()"
  />
</div>
</template>
<script>
  import {mapGetters, mapActions} from "vuex"
  import NavBar from "./components/NavBar.vue"
  import AlertBox from "./components/AlertBox.vue"
  import Modal from "./components/Modal.vue"
  import Report from "./components/Report.vue"
  export default {
    name: "App",
    components: {
      NavBar,
      AlertBox,
      Modal,
      Report,
    },
    methods:{
      ...mapGetters([ 
            "isAccess",
            "isDisplayed"
        ]),
      ...mapActions([
        "showForm"
      ])
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
  .fa-circle-question {
    position: fixed;
    bottom: 50px;
    color:#0d6efd;
    right:30px;
  }
</style>
