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
                return this.modelValue
            },
            set(val){
                console.log(val)
                this.$emit("update:modelValue", val)
            }
        }
    }
}
</script>