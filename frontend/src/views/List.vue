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
                    params: {id: refuel.ID}}">
                    <div class="card text-center">
                        <CardHeader
                        :header="refuel.Date"
                        />
                        <i @click="onDelete(refuel.ID)" class="fas fa-times"></i>
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
            search: "",
        }
    },
    methods:{
        ...mapGetters([
            "isAccess"
        ]),
        ...mapActions([
            "makeFetch",
            "alertSuccess",
        ]),
        async onDelete(id){ //! not eddited yet
            if (confirm(`Are you sure you want to delete ${id}?`)){
                const req = {
                    url: `${this.refuelDepHost}/refuelings/${id}/delete`,
                    method: "POST",
                    data: {"token":this.state.refreshToken},
                    auth: null, //todo access via getter
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
        const req = {
            url: `${this.refuelDepHost}/refuelings`,
            method: "GET",
            data: null,
            auth: this.isAccess(), //todo access via getter
        }
        let results = await this.makeFetch(req)
        if (results){
            this.refuels = results.sort((a,b) => b.RefuelName - a.RefuelName)
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
    #l .fa-times{
        position: absolute;
        top: 8px;
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
    #detail .fa-times {
        position: absolute;
        top: 8px;
        right:8px;

    }
    #detail .fa-file-export{
        position: absolute;
        top: 8px;
        left:8px;
    }
</style>