<template>
    <div> 
        <br>
        <div class="container-flex" >
            <div class="row">
                <div v-for="(refuelDetail,i) in refuelDetails" :key="i" class="col">
                    <div class="card text-center">
                        <CardHeader
                        :header="refuelDetail.Description"
                        />
                        <!-- <a href="#"></a> -->
                        <a href="#"> <i @click="onDelete(refuelDetail.Name)" class="fas fa-times"></i> </a>
                        <Table
                        :map="refuelDetail.CoreConfig"
                        />
                        <div class="card-footer">
                            Download .PDC
                        <a href="#"><i @click="onSave(refuelDetail.PDC, refuelDetail.ID, i)" class="fas fa-file-export"></i></a>
                        </div>
                    </div> <br>
                </div>
                
            </div>
        </div>
        <br>
        <div class="row">  <!-- make it visible on click -->
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
import {mapGetters, mapActions} from "vuex"
import AlertBox from "../components/AlertBox.vue"
import Table from "../components/Refueling/Table.vue"
import CardHeader from "../components/CardHeader.vue"
import CardBody from "../components/CardBody.vue"
import Label from "../components/Label.vue"
import RefuelForm from "../components/Refueling/RefuelForm.vue"
import Button from "../components/Refueling/Button.vue"
import Input from "../components/Refueling/Input.vue"
import TextArea from "../components/Refueling/TextArea.vue"
import { saveFile } from "../helpers"
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
                this.finalForm.refuelNameRef = parseInt(this.$route.params.refuelName) //!!!!!!
            }
        }
    },
    //TODO use the same methods for update 
    methods: {
        ...mapGetters("auth", [
            "isAccess"
        ]),
        ...mapActions([
            "api/makeFetch",
            "alert/alertSuccess"
        ]),
        async getDetails(index){
            const req = {
                url: `${this.refuelDepHost}/refuelings/${this.$route.params.refuelName}/details`,
                method: "GET",
                data: null,
                auth: this.isAccess(),
            }
            let results = await this['api/makeFetch'](req)
            if (results){
                this.refuelDetails = results
                console.log(this.refuelDetails)
                await this.preLoadPDC(this.refuelDetails.at(index).Name, index)
                
                
            }
            
        },
        async preLoadPDC(actName, index) { //
            const req = {
                url: `${this.refuelDepHost}/refuelings/${this.$route.params.refuelName}/${actName}/PDC`,
                method: "GET",
                data: null,
                auth: this.isAccess(),
            }
            let results = await this["api/makeFetch"](req)
            if (results){
                this.refuelDetails.at(index).PDC = results
            }
        },
        async addNewAct(){
            const req = {
                url: `${this.refuelDepHost}/add-act`,
                method: "POST",
                data: this.finalForm,
                auth: this.isAccess(),
            }
            let results = await this['api/makeFetch'](req)
            if (results){
                this.alertSuccess({msg:results.msg})
                this.refuelDetails.at(-1).ID = results.id
            }
        },
        fillFromRefuelForm(obj){
            this.finalForm.description = this.description
            this.finalForm.map = obj.map
            this.finalForm.pdc = obj.pdc
            this.finalForm.fileName = this.refuelDetails.length.toString() //* pass name of new act 
            // this.finalForm.fileName = `${this.$route.params.id}_${this.refuelDetails.length}.PDC` //! its wrong
            this.refuelDetails.push(
                {
                    PDC: this.finalForm.pdc,
                    CoreConfig: this.finalForm.map,
                    Description: this.finalForm.description
                }
            )
            this.addNewAct()
        },
        async onDelete(actName){
            console.log(actName)
            if (confirm(`Are you sure you want to delete ${actName}?`)){
                const req = {
                    url: `${this.refuelDepHost}/refuelings/${this.$route.params.refuelName}/${actName}/delete`,
                    method: "POST",
                    data: null,
                    auth: this.isAccess(),
                }
                let results = await this['api/makeFetch'](req)
                if (results){
                    this.alertSuccess({msg:results})
                    this.refuelDetails = this.refuelDetails.filter(e => e.Name !== actName)
                    await this.preLoadPDC(this.refuelDetails.at(-1).ID, -1)
                }
            }
        },
        onSave(pdc, actId, index){
            let checkPDC = (ref) => {
                if (!ref.PDC) {
                    console.log("calling PDC")
                } else {
                    console.log("ready")
                    clearInterval(intrv)
                    this.save(ref.PDC) //! call for download
                }
            }
            let intrv = setInterval(checkPDC, 100, this.refuelDetails[index])
            let download = new Promise((resolve, reject) => {
                pdc ? resolve("ok") : reject("Whoops!")
            })
            download
            .then(() => this.save(pdc)) //! call for download
            .catch(() => (this.preLoadPDC(actId, index), intrv))
        },
        save: saveFile
    },
}
</script>
<style scoped>
    
    .forms-container {
        width:40%; 
        margin:auto;
    }
    .fa-file-export{
        color: black;
        position: absolute;
        bottom: 13px;
        right:8px;
    }
    .fa-times {
        color: red;
        position: absolute;
        top: 11px;
        right:8px;
    }
</style>