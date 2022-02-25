<template>
    <div class="forms-container">
        <div class="form-floating mb-3">
            <Input
            type="number"
            id="floatingInput"
            @typed="finalForm.name=$event"
            />
            <Label
            for="floatingInput"
            text="Type name of refueling"
            />
        </div>
        <div class="form-floating mb-3">
            <Input
            id="floatingInput"
            type="date"
            @typed="finalForm.date=$event"
            />
            <Label
            for="floatingInput"
            text="Pick date"
            />
        </div>
        <div class="form-floating mb-3">
            <TextArea
            id="floatingTextarea"
            @typed="finalForm.acts[1].description=$event"
            />
            <Label
            for="floatingTextarea"
            text="Comments for first step"
            
            />
        </div>
        <div class="row">
            <div class="col">
                <Button
                text="Back"
                @click="$emit('backRefuel')"
                />
            </div>
            <div class="col">
                <Button
                text="Submit"
                @click="record"
                />
            </div>
        </div>
    </div>
</template>
<script>
import Button from "./Button.vue"
import Input from "./Input.vue"
import Select from "./Select.vue"
import Label from "../Label.vue"
import TextArea from "./TextArea.vue"
export default {
    name: "ConfirmationForm",
    components: {
        Button,
        Input,
        Select,
        Label,
        TextArea,
    },
    props:["modelValue"],
    emits:["backRefuel", "confForm"],

    data(){
        return {
            selectOpt:[
                {
                    "name": "New Refueling",
                    "value": "new",
                },
                {
                    "name": "Update Existing",
                    "value": "update",
                },

            ],
        }
    },
    computed:{
        finalForm:{
            get(){
                return this.modelValue
            }
        }
    },
    methods:{
        changeForm(selected){
            switch(selected){
                case "new":
                    this.addNew=true
                    break;
                case "update":
                    this.addNew=false;
                    break;    
            }
        },
        record(){
            //*Adding requsets
            console.log(this.finalForm)
            const request = new Request(
            `${this.refuelDepHost}/add`,
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
            .then(response => 
                {   console.log(response.status)
                    return (this.$emit("response", 
                        {
                            statusCode: response.status,
                            status: true,
                            redirect: response.ok ? true : false
                        }), response.json())
                }
            )
            .then(data => this.$emit("alertMsg", data)) //* pass alert msg
            .catch((error) => console.log(`catched errors: ${error}`))
        },
    },
    watch:{
        'finalForm.name':{
            handler(){
                this.finalForm.acts.forEach((e,i) => e.fileName=`${this.finalForm.name}_${i}.PDC`)
            }
        }
    }

}
</script>