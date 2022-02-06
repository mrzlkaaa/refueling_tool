<template>
    <div id="detail"> 
        <br>
        <div class="container-flex" >
            <div class="row">
                <div v-for="(refuelDetail,i) in refuelDetails" :key="i" class="col">
                    <div class="card text-center">
                        <CardHeader
                        :header="refuelDetail.Description"
                        />
                        <i @click="onDelete(refuelDetail.ID)" class="fas fa-times"></i>
                        <Table
                        :map="refuelDetail.CoreConfig"
                        />
                    </div> <br>
                </div>
            </div>
        </div>
        <br>
        <div class="row">
            <div class="col">
                 <RefuelForm
                ref="newConfig"
                :pdc="refuelDetails.at(-1).PDC"
                @refuelForm="fillFromRefuelForm"
                />
                <div class="forms-container">
                    <div class="form-floating mb-3">
                        <TextArea
                        id="floatingTextarea"
                        @typed="this.description=$event"
                        />
                        <Label
                        for="floatingTextarea"
                        text="Comments for first step"
                        />
                    </div>
                    <Button
                    text="Next"
                    width="20%"
                    @click="$refs.newConfig.getNewConfig()"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Table from "../components/Refueling/Table.vue"
import CardHeader from "../components/CardHeader.vue"
import CardBody from "../components/CardBody.vue"
import UpdateForm from "../components/Refueling/UpdateForm.vue"
import RefuelForm from "../components/Refueling/RefuelForm.vue"
import Button from "../components/Refueling/Button.vue"
import Input from "../components/Refueling/Input.vue"
import TextArea from "../components/Refueling/TextArea.vue"
export default {
    name: "Detail",
    components: {
        Table,
        CardHeader,
        CardBody,
        UpdateForm,
        RefuelForm,
        Button,
        Input,
        TextArea,
    },
    props: ["id"], //TODO add excption if ID is not given
    data(){
        return {
            refuelDetails: [{
                pdc: [],
            },],
            finalForm:{},
            description:'',
        }
    },
    mounted(){
        console.log("ready")
        console.log(this.$route.params)
        this.getDetails(-1)
    },
    watch: {
        id(){
            console.log("changed")
            this.getDetails(-1)
        },
        refuelDetails:{
            deep: true,
            handler(){
                this.finalForm.refuelId = this.$route.params.id
            }
        }
    },
    //TODO use the same methods for update 
    methods: {
        getDetails(index){
            fetch(`http://localhost:8888/refuelings/${this.$route.params.id}/details`)
            .then(response => response.json())
            .then(data => {
                this.refuelDetails = data
                return (this.preLoadPDC(this.refuelDetails.at(index).ID, index))})
            .catch(error => console.error(error))
            
        },
        preLoadPDC(actId, index) {
            console.log(actId)
            console.log("called")
            fetch(`http://localhost:8888/refuelings/${this.$route.params.id}/${actId}/PDC`)
            .then(response => response.json())
            .then(data => (this.refuelDetails.at(index).PDC = data, console.log(this.refuelDetails.at(index))))
            .catch(error => console.error(error))
        },
        async addNewAct(){

        },
        fillFromRefuelForm(obj){
            this.finalForm.description = this.description
            this.finalForm.map = obj.map
            this.finalForm.pdc = obj.pdc
            this.finalForm.name = `${this.$route.params.id}_${this.refuelDetails.length}.PDC`
            this.refuelDetails.push(
                {
                    ID: (() => this.refuelDetails.at(-1).ID)()+1,
                    PDC: this.finalForm.pdc,
                    CoreConfig: this.finalForm.map,
                    Description: this.finalForm.description
                }
            )
            console.log(this.refuelDetails)
            console.log(this.finalForm)
        },
        onDelete(actId){
            console.log(actId)
            this.refuelDetails = this.refuelDetails.filter(e => e.ID !== actId)
        }
    },
}
</script>
<style>
    #detail .table {
        margin: auto;
        width: 350px;
    }
    #detail .table td {
        height:40px;
    }
    .card .fa-times {
        position: absolute;
        top: 8px;
        right:8px;

    }
    .forms-container {
        width:40%; 
        margin:auto;
    }
</style>