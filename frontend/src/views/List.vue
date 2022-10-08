<template>
    <div class="container">
        <div class="row">
            <div id="l" class="col col-3">
                <br>
                <Input
                type="text"
                cls="form-control me-2"
                placeholder="Search"
                aria-label="Search"
                @typed="search=$event"
                />
                <br>
                <router-link v-for="(refuel, i) in refuels" :key="i" :to="{name: 'Detail', 
                    params: {refuelName: refuel.RefuelName}}">
                    <div class="card text-center">
                        <CardHeader
                        :header="refuel.Date"
                        />
                        <i @click="onDelete(refuel.RefuelName)" class="fas fa-times"></i>
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
import { mapActions, mapGetters } from 'vuex'
import Input from "../components/Refueling/Input.vue"
import CardHeader from "../components/CardHeader.vue"
import CardBody from "../components/CardBody.vue"
import AlertBox from "../components/AlertBox.vue"
import { sortRefuelings } from "../helpers"

export default {
    name: "List",
    components: {
        Input,
        CardHeader,
        CardBody,
        AlertBox,
    },
    data(){
        return {
            dat:{
                code : 200,
                msg: "",
            },
            refuels: Object,
            list: Array,
            search: "",
        }
    },
    methods:{
        ...mapGetters("auth", [
            "isAccess"
        ]),
        ...mapActions("api", [
            "makeFetch"
        ]),
        async onDelete(refuelName){ //! not eddited yet
            if (confirm(`Are you sure you want to delete ${refuelName}?`)){
                const req = {
                    url: `${this.refuelDepHost}/refuelings/${refuelName}/delete`,
                    method: "POST",
                    data: null,
                    auth: this.isAccess(),
                }
                let results = await this.makeFetch(req)

                if (results){
                    this.alertSuccess({msg:results})
                    this.refuels = this.refuels.filter(e => e.ID !== id)
                }
            }
        }
    },
    //TODO add computed hook to call alert box
    async created(){
        console.log(this.isAccess())
        const req = {
            url: `${this.refuelDepHost}/refuelings`,
            method: "GET",
            data: null,
            auth: this.isAccess(), //todo access via getter
        }
        let results = await this.makeFetch(req)
        if (results){
            console.log(results)
            this.refuels = results.sort((a,b) => sortRefuelings(a.RefuelName, b.RefuelName)) //b.RefuelName - a.RefuelName)
            this.backUpRefuels = JSON.parse(JSON.stringify(this.refuels))
        }
    },
    watch:{
        search(){
            //* search by name
            this.refuels = this.backUpRefuels
            this.refuels = this.refuels.filter(e => this.search.length != 0 ? e.RefuelName.toString().includes(this.search) : this.refuels)
        }
    },
}
</script>
<style>
    .container {
        margin-top: 60px;
    }
    #r {
    }
    .fa-times{
        color: red;
        position: absolute;
        top: 12px;
        right:8px;
    }
    .container-flex {
        width: 100%;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-around;
        height: 100%;
        align-items: stretch;
    }
    .container-flex .col {
        margin: auto;
        flex: 0 0 50%;
    }
    /* #detail .fa-times {
        position: absolute;
        top: 8px;
        right:8px;
    }
    #detail .fa-file-export{
        position: absolute;
        top: 8px;
        left:8px;
    } */
</style>