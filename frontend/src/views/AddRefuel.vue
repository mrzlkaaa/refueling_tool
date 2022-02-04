<template>
    <div id="addRefuel" class="main-box">
        <div v-if="alert.status">
            <AlertBox
            :code="alert.statusCode"
            :text="alert.msg"
            />
        </div>
        <div class="card text-center">
            <CardHeader
            header="Add new instance" 
            />
            <div class="card-body">
                <br>
                <!-- <span>{{fileDataUpd}}</span> -->
                <div v-if="!initialData.status" class="row">
                    <div class="col">
                        <Input
                        type="file"
                        @change="upload($event)"
                        />
                    </div>
                    <div class="col">
                        <form @click.prevent="submitFile">
                            <Button
                            text="Upload"
                            />
                        </form>
                    </div>
                </div>
                <div v-if="initialData.status">
                    <div class="container-flex" >
                        <div class="row">
                            <div class="col">
                                <Table
                                :map="initialData.map"
                                />
                            </div>
                        </div>
                        <div v-if="firstStep.status" class="row">
                            <div class="col">
                                <Table
                                :map="firstStep.map"
                                />
                            </div>
                        </div>
                    </div>
                    <br>
                    <div class="row">
                        <div v-if="showRefForm" class="col">
                            <RefuelForm
                            ref="newConfig"
                            :pdc="initialData.pdc"
                            @refuelForm="fillFromRefuelForm"
                            />
                            <div class="form-container">
                                <Button
                                text="Next"
                                width="20%"
                                @click="$refs.newConfig.getNewConfig()"
                                />
                            </div>
                        </div>
                        <div v-else class="col">
                            <ConfirmationForm
                            v-model="finalForm"
                            @response="applyReponse"
                            @alertMsg="alert.msg=$event"
                            @backRefuel="showRefForm=!showRefForm"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Input from "../components/Refueling/Input.vue"
    import Button from "../components/Refueling/Button.vue"
    import Table from "../components/Refueling/Table.vue"
    import RefuelForm from "../components/Refueling/RefuelForm.vue"
    import ConfirmationForm from "../components/Refueling/ConfirmationForm.vue"
    import AlertBox from "../components/Refueling/AlertBox.vue"
    

    export default {
        name: "AddRefuel",
        data:function() {
            return {
                finalForm: {
                    name:"",
                    date: "",
                    acts: []
                },
                postFile: Object,
                initialData: {
                    status: false,
                },
                firstStep:{
                    status: false,
                },
                showRefForm: true,
                alert: {
                    status: false,
                    statusCode: 200,
                    msg: '',
                }
            }
        },
        components: {
            Input,
            Button,
            Table,
            RefuelForm,
            ConfirmationForm,
            AlertBox,
        },
        computed: {
            fileDataUpd(){
                return this.initialData.status ? "yes" : "no"
            }
        },
        methods: {
            submitFile() {
                let formData = new FormData()
                formData.append("file", this.postFile)
                const request = new Request(
                "http://localhost:8000/average",
            {
                method: "POST",
                headers: { 
                        'Accept': 'application/json',
                        'Access-Control-Allow-Origin': '*' },
                body: formData
            }
            );
            fetch(request)
                .then(response => response.json())
                .then(data => (console.log(data), this.initialData=data, 
                    this.finalForm.acts.push(this.initialData)))
                .catch((error) => console.log(error.message))
            },
            upload(e) {this.postFile = e.target.files[0]},
            fillFromRefuelForm(obj){
                this.firstStep = obj
                this.finalForm.acts.push(this.firstStep)
                this.showRefForm = !this.showRefForm
            },
            counter(started){
                setInterval(() => {
                    this.alert.time=Date.now()-started
                    }, 100)
            },
            applyReponse(e){
                this.alert.statusCode=e.statusCode
                this.alert.status = e.status
                if (e.redirect) {
                    console.log("initiated")
                    //TODO redirect to exlicit url like <<refuels/ID/detail>>
                    setTimeout(()=>{this.$router.push({name: "List"})}, 3000) 
                }
            }
        }
    }
</script>
<style>
    .container-flex {
        width: 100%;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-around;
        height: 100%;
        align-items: stretch;
    }
    #addRefuel .col {
        width:50%;
    }
    .slide-enter-active, .slide-leave-active {
        transition: opacity 1s;
    }
    .slide-enter, .slide-leave-to {
        /* transform: translateX(-200px); */
        opacity: 0;
    }
    #addRefuel .table {
        margin: auto;
        width: 350px;
    }
    #addRefuel .table td {
        height:40px;
    }
</style>
