<template>
    <select v-model="selectedName" class="form-select" aria-label=".form-select-lg example" @change="fcUpdated">
        <!-- <option selected> {{selected}} </option> -->
        <option selected value> Choose any </option>
        <option v-for="(name, index) in refuelingsList" v-bind:key="index" :value="name"> {{name}} </option>
    </select>
</template>

<script>
export default {
    Name: "Select",
    props: ["refuelings-list"],
    data() {
        return {
            selectedName:"",
        }
    },
    methods: {
        fcUpdated() {
            this.$emit("fcName", this.selectedName)
            console.log(this.selectedName)
        }
    }
}
</script>