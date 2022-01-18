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
    Name: "SelectW",
    props: ["data"],
    data() {
        return {
            selectedName:"",
        }
    },
    methods: {
        selectChanged() {
            this.$emit("weekName", this.selectedName)
            console.log("weekName sent")
            console.log(this.selectedName)
        },
    }
}
</script>