<template>
    <div class="container">
        <AlertBox
        :info="getAlert()"
        />
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
    //TODO add computed hook to call alert box
    created(){

        const request = new Request(
            `${this.refuelDepHost}/refuelings`,
            {
                method: "GET",
                headers: {
                        "Authorization": this.$store.state.auth.accessToken,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        }
            }
        )
        fetch(request)
            .then(response => {
                this.dat.code=response.status
                return response.json()
            })
            .then(data => {
                this.dat.msg = data
                switch (data){
                    case "token is expired":
                        this.$store.dispatch("refreshTokens", this.authDepHost)
                        break;
                    case "you are not eligible for this service":
                        this.$store.dispatch("alertWarning", this.dat)
                        //todo add smth like "contact admin" and form appears
                        break;
                    default:
                        if (this.dat.code==200){
                            this.refuels = data.sort((a,b) => b.RefuelName - a.RefuelName)
                        }
                        else {
                            setTimeout(this.$router.push, 4000, {name:"Login"})
                        }
                        
                }
            })
            .catch(error => console.log(error.message))
        // this.backUpRefuels = this.refuels

    },
    methods:{
         ...mapGetters([
            "getAlert"
        ]),
        ...mapActions([
            "makeFetch"
        ]),
        onDelete(id){
            if (confirm(`Are you sure you want to delete ${id}?`)){
                const request = new Request(
                `${this.refuelDepHost}/refuelings/${id}/delete`,
                    {
                        method: "POST",
                        headers: { 
                                'Accept': 'application/json',
                                "Content-Type": "application/json",
                                },
                        body: JSON.stringify(id)
                    }
                )
                //! is not fixed to new style
                fetch(request)
                .then(response => {
                    this.alert.statusCode = response.status
                    this.alert.status = true
                    if (response.status==200 ) {
                        this.refuels = this.refuels.filter(e => e.ID !== id)
                        // this.preLoadPDC(this.refuelDetails.at(-1).ID, -1)
                    }
                    return response.json() 
                })
                .then(data => (console.log(data), this.alert.msg = data))
                .catch(error => console.error(error))
            }
        }
    },
    watch:{
        search(){
            //* search by year and name
            console.log(this.$store.state.alert)
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