<template>
    <div class="container">
        <div class="row">
            <div id="l" class="col col-3">
                <br>
                <Input
                type="search"
                cls="form-control me-2"
                placeholder="Search"
                aria-label="Search"
                />
                <br>
                <router-link v-for="(refuel, i) in refuels" :key="i" :to="{name: 'Detail', 
                    params: {id: refuel.ID, name:refuel.RefuelName}}">
                    <div  class="card text-center">
                        <CardHeader
                        :header="refuel.Date"
                        />
                        <CardBody
                        :text="refuel.RefuelName"
                        />
                    </div>
                    <br>
                </router-link>
            </div>
            <div id="r" class="col col-xl-">
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>
<script>
import Input from "../components/Refueling/Input.vue"
import CardHeader from "../components/CardHeader.vue"
import CardBody from "../components/CardBody.vue"
export default {
    name: "List",
    components: {
        Input,
        CardHeader,
        CardBody,
    },
    data(){
        return {
            refuels: Object
        }
    },
    mounted(){
            fetch("http://localhost:8888/refuelings")
            .then(response => response.json())
            .then(data => this.refuels = data)
            .catch(error => console.log(error.message))
    }
}
</script>
<style>
    .container {
        margin-top: 60px;
    }

    #r {
    }
    #l {
    }
</style>