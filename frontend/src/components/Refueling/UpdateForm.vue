<template>
    <div class="forms-container">
            <div class="form-floating mb-3">
                <Select
                :optns="selectOpt"
                @selected="assignSelect"
                />
                <Label
                for="floatingSelect"
                text="Choose option"
                />
            </div>
            <div class="form-floating mb-3">
                <Input
                name="numbers"
                id="floatingInput"
                @typed="assignInput"
                />
                <Label
                for="floatingInput"
                text="FA numbers"
                />
            </div>
            <div class="form-floating mb-3">
                <TextArea
                id="floatingTextarea"
                />
                <Label
                for="floatingTextarea"
                text="Any Comments"
                />
            </div>
            <Button
            text="Submit"
            />
        </div>
</template>
<script>
    import Input from "./Input.vue"
    import Select from "./Select.vue"
    import Label from "./Label.vue"
    import Button from "./Button.vue"    
    import TextArea from "./TextArea.vue"
export default {
    name: "UpdateForm",
    components: {
        Input,
        Select,
        Label,
        Button,
        TextArea,
    },
    data(){
        return {
            selectOpt:[
                    {name:'Fresh fuel', value:'fresh'},
                    {name:'Swap', value:'swap'},
                ],
        }
    }
}
</script>