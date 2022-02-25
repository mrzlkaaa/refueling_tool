<template>
    <div id="detail"> 
        <br>
        <div v-if="alert.status">
            <AlertBox
            :code="alert.statusCode"
            :text="alert.msg"
            :time="alert.time"
            @hide="alert.status=$event.status,
                   alert.msg=$event.msg"
            />
        </div>
        <div class="container-flex" >
            <div class="row">
                <div v-for="(refuelDetail,i) in refuelDetails" :key="i" class="col">
                    <div class="card text-center">
                        <CardHeader
                        :header="refuelDetail.Description"
                        />
                        <i @click="onSave(refuelDetail.PDC, refuelDetail.ID, i)" class="fas fa-file-export"></i>
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
                        text="Comments"
                        />
                    </div>
                    <Button
                    text="Add"
                    width="20%"
                    @click="$refs.newConfig.getNewConfig()"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import AlertBox from "../components/AlertBox.vue"
import Table from "../components/Refueling/Table.vue"
import CardHeader from "../components/CardHeader.vue"
import CardBody from "../components/CardBody.vue"
import Label from "../components/Label.vue"
import RefuelForm from "../components/Refueling/RefuelForm.vue"
import Button from "../components/Refueling/Button.vue"
import Input from "../components/Refueling/Input.vue"
import TextArea from "../components/Refueling/TextArea.vue"
import { saveFile } from "../components/helpers"
// require("downloadjs")(data, strFileName, strMimeType)

export default {
    name: "Detail",
    components: {
        Table,
        CardHeader,
        CardBody,
        RefuelForm,
        Button,
        Input,
        Label,
        TextArea,
        AlertBox,
    },
    props: ["id"], //TODO add excption if ID is not given
    data(){
        return {
            refuelDetails: [{
                pdc: [],
            },],
            finalForm:{},
            description:'',
            alert: {
                status: false,
                statusCode: 200,
                msg: '',
                time: 5,
            },
            url:"",
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
                this.finalForm.refuelId = parseInt(this.$route.params.id)
            }
        }
    },
    //TODO use the same methods for update 
    methods: {
        getDetails(index){
            fetch(`${this.refuelDepHost}/refuelings/${this.$route.params.id}/details`)
            .then(response => response.json())
            .then(data => {
                this.refuelDetails = data
                return (this.preLoadPDC(this.refuelDetails.at(index).ID, index))})
            .catch(error => console.error(error))
            
        },
        preLoadPDC(actId, index) {
            console.log(actId)
            console.log("called")
            fetch(`${this.refuelDepHost}/refuelings/${this.$route.params.id}/${actId}/PDC`)
            .then(response => response.json())
            .then(data => (this.refuelDetails.at(index).PDC = data, console.log(this.refuelDetails.at(index))))
            .catch(error => console.error(error))
        },
        addNewAct(){
            const request = new Request(
                `${this.refuelDepHost}/add-act`,
                    {
                        method: "POST",
                        headers: { 
                                'Accept': 'application/json',
                                "Content-Type": "application/json",
                                },
                        body: JSON.stringify(this.finalForm)
                    }
            )
            fetch(request)
            .then(response => {
                this.alert.statusCode = response.status
                this.alert.status = true
                return response.json()
            })
            .then(data => (
                this.alert.msg = data.msg,
                this.refuelDetails.at(-1).ID = data.id))
            .catch(error => console.error(error))
        },
        fillFromRefuelForm(obj){
            this.finalForm.description = this.description
            this.finalForm.map = obj.map
            this.finalForm.pdc = obj.pdc
            this.finalForm.fileName = `${this.$route.params.id}_${this.refuelDetails.length}.PDC`
            this.refuelDetails.push(
                {
                    PDC: this.finalForm.pdc,
                    CoreConfig: this.finalForm.map,
                    Description: this.finalForm.description
                }
            )
            this.addNewAct()
        },
        onDelete(actId){
            console.log(actId)
            if (confirm(`Are you sure you want to delete ${actId}?`)){
                const request = new Request(
                `${this.refuelDepHost}/refuelings/${this.$route.params.id}/${actId}/delete`,
                    {
                        method: "POST",
                        headers: { 
                                'Accept': 'application/json',
                                "Content-Type": "application/json",
                                },
                        body: JSON.stringify(actId)
                    }
                )
                fetch(request)
                .then(response => {
                    this.alert.statusCode = response.status
                    this.alert.status = true
                    if (response.status==200 ) {
                        this.refuelDetails = this.refuelDetails.filter(e => e.ID !== actId)
                        this.preLoadPDC(this.refuelDetails.at(-1).ID, -1)
                    }
                    return response.json() 
                })
                .then(data => (console.log(data), this.alert.msg = data))
                .catch(error => console.error(error))
            }
        },
        onSave(pdc, actId, index){
            let checkPDC = (ref) => {
                if (!ref.PDC) {
                    console.log("calling PDC")
                } else {
                    console.log("ready")
                    clearInterval(intrv)
                    this.save(ref.PDC)
                }
            }
            let intrv = setInterval(checkPDC, 100, this.refuelDetails[index])
            let download = new Promise((resolve, reject) => {
                pdc ? resolve("ok") : reject("Whoops!")
            })
            download
            .then(() => this.save(pdc))
            .catch(() => (this.preLoadPDC(actId, index), intrv))
        },
        save: saveFile
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