<template>
    <div class="main-box">
        <div class="card text-center">
            <CardHeader
            header="File uploading" 
            />
            <div class="card-body">
                <CardTitle
                title="Attach your local .PDC file to start use service"
                />
                <br>
                <span>{{fileDataUpd}}</span>
                <div v-if="!fileData.status" class="row">
                    <div class="col">
                        <Input
                        type="file"
                        @change="upload($event)"
                        />
                    </div>
                    <div class="col">
                        <form @click.prevent="submit">
                            <Button/>
                        </form>
                    </div>
                </div>
                <div v-if="fileData.status">
                    <div class="row">
                        <div class="col">
                            <Table
                            :map="fileData.obj.map"
                            />
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <div class="form-floating mb-3">
							<select name='options' class="form-select" id="floatingSelect" aria-label="Floating label select example">
								<option value='fresh'> Fresh fuel </option>
								<option value='swap'> Swap </option>
							</select>
							<label for="floatingSelect">Choose option</label>
							</div>
							<div class="text-inputs-refuel form-floating mb-3">
							<input type="text" name="numbers" class="form-control" id="floatingInput" placeholder="Typing...">
							<label for="floatingInput">FA numbers</label>
							</div>
							<input type="submit" class="text_inputs btn btn-primary">
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
    import Label from "../components/Refueling/Label.vue"

    export default {
        name: "AddRefuel",
        data:function() {
            return {
                postForm: Object,
                fileData: {
                    status: false,
                },
            }
        },
        components: {
            CardHeader,
            CardTitle,
            Input,
            Button,
            Table,
            Label,
        },
        computed: {
            fileDataUpd(){
                return this.fileData.status ? "yes" : "no"
            }
        },
        methods: {
            submit() {
                let formData = new FormData()
                formData.append("file", this.postForm)
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
                .then(data => this.fileData=data)
                .catch((error) => console.log(error.message))
            // console.log(this.fileData)
            },
            upload(e) {this.postForm = e.target.files[0]}
        }
    }
</script>
<style>
    .row{
        position: relative;
    }
    .col {
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
