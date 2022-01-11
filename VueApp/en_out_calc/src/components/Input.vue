<template>
    <input type="text" class="form-control" v-model="inputValue">
</template>

<script>
export default {
    name: "Input",
    props: ["modelValue"],
    computed:{
        inputValue:{
            get(){
                console.log(typeof(this.modelValue))
                return this.modelValue
            },
            set(val){
                console.log(this.modelValue)
                this.$emit("update:modelValue", val)
            }
        }
    }
}
</script>