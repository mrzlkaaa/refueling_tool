<template>
     <div class="container" style="position:relative">
        <div class="row">
            <div id="l" class="col col-3">
                <br>
                <router-link v-for="(s, i) in settings" :key="i" :to="{name: s}">
                    <div class="card text-center">
                        <div class="card text-center">
                            <CardHeader
                            :header="s"
                            />
                            <!-- <i @click="onDelete(refuel.ID)" class="fas fa-times"></i> -->
                            <!-- <CardBody
                            :text="refuel.RefuelName"
                            /> -->
                        </div>
                    </div>
                </router-link>
            </div>
            <div id="r" class="col col-xl"><br>
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>
<script>
import AlertBox from "../components/AlertBox.vue"
import CardHeader from "../components/CardHeader.vue"
import CardBody from "../components/CardBody.vue"
export default {
    name: "Settings",
    components:{
        AlertBox,
        CardHeader,
        CardBody,
    }, 
    data(){
        return {
            settings:[
                "General",
                "Users"
            ]
        }
    },
    computed:{
        alert(){
            return this.$store.state.alert
        }
    }
}
</script>