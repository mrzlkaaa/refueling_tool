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
                <!-- <UpdateForm
                :latterInstance="refuelDetails.at(-1)"
                /> -->
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
    props: ["id", "name"], //TODO add excption if ID is not given
    data(){
        return {
            refuelDetails: [{
                pdc: [],
            }],
            finalForm:{},
            description:'',
        }
    },
    mounted(){
        console.log("ready")
        this.getDetails(this.id)
    },
    watch: {
        id(){
            console.log("changed")
            this.getDetails(this.id, -1) //* second arg is slice index
        },
        refuelDetails:{
            deep: true,
            handler(){
                this.finalForm.refuelId = this.id
            }
        }
    },
    //TODO use the same methods for update 
    methods: {
        getDetails(id, index){
            fetch(`http://localhost:8888/refuelings/${id}/details`)
            .then(response => response.json())
            .then(data => {
                this.preLoadPDC(data.at(index).ID, index)
                return (this.refuelDetails = data, console.log(data, this.refuelDetails))})
            .catch(error => console.error(error))
            
        },
        preLoadPDC(id, index) {
            console.log(this.refuelDetails)
            console.log("called")
            fetch(`http://localhost:8888/refuelings/${id}/PDC`)
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
            this.finalForm.name = `${this.name}_${this.refuelDetails.length}.PDC`
            this.refuelDetails.push(
                {
                    PDC: this.finalForm.pdc,
                    CoreConfig: this.finalForm.map,
                    Description: this.finalForm.description
                }
            )
            console.log(this.finalForm)
        },
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
    .forms-container {
        width:40%; 
        margin:auto;
    }
</style>