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
                <UpdateForm
                :latterInstance="refuelDetails.at(-1)"
                />
            </div>
        </div>
    </div>
</template>
<script>
import Table from "../components/Refueling/Table.vue"
import CardHeader from "../components/CardHeader.vue"
import CardBody from "../components/CardBody.vue"
import UpdateForm from "../components/Refueling/UpdateForm.vue"
import Input from "../components/Refueling/Input.vue"
import TextArea from "../components/Refueling/TextArea.vue"
export default {
    name: "Detail",
    components: {
        Table,
        CardHeader,
        CardBody,
        UpdateForm,
        Input,
        TextArea,
    },
    props: ["id"],
    data(){
        return {
            refuelDetails: [{
                ID: 1234,
            }],
        }
    },
    created(){
        console.log("ready")
        this.getDetails(this.id)
    },
    watch: {
        id(){
            console.log("changed")
            this.getDetails(this.id, -1) //* second arg is slice index
        }
    },
    //TODO use the same methods for update 
    methods: {
        getDetails(id, index){
            fetch(`http://localhost:8888/refuelings/${id}/details`)
            .then(response => response.json())
            .then(data => {
                this.preLoadPDC(data.at(index).ID, index)
                return this.refuelDetails = data})
            .catch(error => console.error(error))
        },
        preLoadPDC(id, index) {
            console.log("called")
            fetch(`http://localhost:8888/refuelings/${id}/PDC`)
            .then(response => response.json())
            .then(data => (this.refuelDetails.at(index).PDC = data, console.log(this.refuelDetails.at(index))))
            .catch(error => console.error(error))
        },
    }
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
</style>