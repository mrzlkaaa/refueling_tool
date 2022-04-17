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
                this.$emit("update:modelValue", val)
                
            }
        }
    }       
}
</script>
<style>
    .err:focus {
        box-shadow: 0 1px 1px rgba(238, 5, 5, 0.9) inset, 0 0 8px rgba(236, 14, 14, 0.8);
    }
</style>