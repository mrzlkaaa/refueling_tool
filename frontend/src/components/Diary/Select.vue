<template>
    <select v-model="selectedName" class="form-select" aria-label=".form-select-lg example" 
    @change="$emit('selected', selectedName)">
        <option selected value> Choose any </option>
        <option v-for="(name, index) in data" v-bind:key="index" :value="name"> {{display=='value' ? name : index }} </option>
    </select>
</template>

<script>
export default {
    Name: "SelectFC",
    props: ["data", "display"],
    emits:["selected"],
    data() {
        return {
            selectedName:"",
        }
    },
    methods: {
        selectChanged() {
            this.$emit("selected", this.selectedName)
            console.log("fcName sent")
            console.log(this.selectedName)
        },
    },
    watch:{
        //todo needs date formatting
        data(){
            if (this.display == "key") {
                
            }
            
        }
    }
}
</script>