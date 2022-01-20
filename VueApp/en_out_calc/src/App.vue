<template>
  <div>
    <h3> Calculate Thermal Power Output </h3>
    <div class="card text-center">
        <div class="card-header">
          {{msg}} weekly data
        </div>
        <div class="card-body">
          <AddUpdate
            @msg="changeMsg"
            />
        </div>
    </div>
  </div>
</template>

<script>
import AddUpdate from "./components/AddUpdate.vue"

export default {
  name: 'App',
  components: {
    AddUpdate,
  },
  data() {
    return {
      msg: ""
    }
  },
  methods: {
    changeMsg(val){
      this.msg = val
    }
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
.row {
  position: relative;
}
.col .fa-times {
  position: absolute;
  top:0;
  right:15px;
  color:red;
}
.btn {
  width:25%;
}
.col {
  width:33%;
}
</style>
