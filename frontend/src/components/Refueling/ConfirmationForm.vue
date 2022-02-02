<template>
    <div class="forms-container">
        <div class="form-floating mb-3">
            <Input
            type="number"
            id="floatingInput"
            @typed="formData.name=$event"
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
            @typed="formData.date=$event"
            />
            <Label
            for="floatingInput"
            text="Pick date"
            />
        </div>
        <div class="form-floating mb-3">
            <TextArea
            id="floatingTextarea"
            @typed="formData.description=$event"
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
                @click="$emit('confForm', formData)"
                />
            </div>
        </div>
    </div>
</template>
<script>
import Button from "./Button.vue"
import Input from "./Input.vue"
import Select from "./Select.vue"
import Label from "./Label.vue"
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
    emits:["backRefuel", "confForm"],
    data(){
        return {
            formData: {
                name:"",
                date:"",
                description:"",
            },
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
    },
    watch:{
        formData:{
            deep:true,
            handler(){
                console.log(this.formData)
            }
        }   
    }

}
</script>