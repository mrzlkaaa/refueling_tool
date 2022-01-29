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
                <div v-if="burnupMap.length == 0" class="row">
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
            </div>
        
        </div>
    </div>
</template>

<script>
    import CardHeader from "../components/CardHeader.vue"
    import CardTitle from "../components/CardTitle.vue"
    import Input from "../components/Refueling/Input.vue"
    import Button from "../components/Refueling/Button.vue"
    export default {
        name: "AddRefuel",
        data:function() {
            return {
                postForm: Object,
                burnupMap: [],
                // form: "",
            }
        },
        components: {
            CardHeader,
            CardTitle,
            Input,
            Button,
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
                .then(data => console.log(data))
                .catch((error) => console.log(error.message))
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
</style>