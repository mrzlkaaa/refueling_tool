<template>
    <div class="main-box">
        <div class="card text-center">
            <CardHeader
            header="Add new instance" 
            />
            <div class="card-body">
                <!-- <CardTitle
                title="Attach your local .PDC file to start use service"
                /> -->
                <br>
                <span>{{fileDataUpd}}</span>
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
                            :refuelName="initialData.fileName"
                            @refuelForm="fillFromRefuelForm"
                            />
                        </div>
                        <div v-else class="col">
                            <ConfirmationForm
                            @confForm="fillFromConfForm"
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
    import CardHeader from "../components/CardHeader.vue"
    import CardTitle from "../components/CardTitle.vue"
    import Input from "../components/Refueling/Input.vue"
    import Button from "../components/Refueling/Button.vue"
    import Table from "../components/Refueling/Table.vue"
    import RefuelForm from "../components/Refueling/RefuelForm.vue"
    import ConfirmationForm from "../components/Refueling/ConfirmationForm.vue"
    

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
            }
        },
        components: {
            CardHeader,
            CardTitle,
            Input,
            Button,
            Table,
            RefuelForm,
            ConfirmationForm,
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
                .then(data => (this.initialData=data, 
                    this.finalForm.acts.push(this.initialData)))
                .catch((error) => console.log(error.message))
            console.log(this.initialData)
            },
            upload(e) {this.postFile = e.target.files[0]},
            fillFromRefuelForm(obj){
                this.firstStep = obj
                this.finalForm.acts.push(this.firstStep)
                this.showRefForm = !this.showRefForm
            },
            fillFromConfForm(obj){
                this.finalForm.name=obj.name
                this.finalForm.date=obj.date
                this.finalForm.acts.at(0).fileName = `${this.finalForm.name}_${this.finalForm.acts.at(0).fileName}`
                this.finalForm.acts.at(-1).fileName = `${this.finalForm.name}_${this.finalForm.acts.at(-1).fileName}`
                this.finalForm.acts.at(-1).description = obj.description
                console.log(this.finalForm)

                const request = new Request(
                "http://localhost:8888/add",
                {
                    method: "POST",
                    headers: { 
                            // 'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            },
                    body: JSON.stringify(this.finalForm)
                }
                );
                fetch(request)
                    .then(response => response.json())
                    // .then(data => (this.initialData=data, 
                    //     this.finalForm.acts.push(this.initialData)))
                    .catch((error) => console.log(error.message))
                
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
    .col {
        /* position:absolute; */
        width:50%;
    }
    .slide-enter-active, .slide-leave-active {
        transition: opacity 1s;
    }
    .slide-enter, .slide-leave-to {
        /* transform: translateX(-200px); */
        opacity: 0;
    }
    .table {
        margin: auto;
        width: 350px;
    }
    .table td {
        height:40px;
    }
    

</style>
