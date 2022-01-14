<template>
    <select v-model="selected" class="form-select" aria-label=".form-select-lg example" @change="FCupdate">
        <option selected> {{selected}} </option>
        <option v-for="(name, index) in names" v-bind:key="index" :value="name"> {{name}} </option>
    </select>
</template>

<script>
export default {
    Name: "Select",
    props: ["modelValue"],
    data() {
        return {
            selected:"Choose one",
        }
    },
    computed:{
        names : {
            get() {
                return this.modelValue
            }
        }
    },
    methods: {
        FCupdate() {
            this.$emit("fcUpdate", this.selected)
            console.log(this.selected)
        }
    }
}
</script>