<template>
    <select v-model="selectedName" class="form-select" aria-label=".form-select-lg example" 
    @change="selectChanged">
        <!-- <option selected> {{selected}} </option> -->
        <option selected value> Choose any </option>
        <option v-for="(name, index) in data" v-bind:key="index" :value="name"> {{name}} </option>
    </select>
</template>

<script>
export default {
    Name: "SelectFC",
    props: ["data"],
    data() {
        return {
            selectedName:"",
        }
    },
    methods: {
        selectChanged() {
            this.$emit("fcName", this.selectedName)
            console.log("fcName sent")
            console.log(this.selectedName)
        },
    }
}
</script>