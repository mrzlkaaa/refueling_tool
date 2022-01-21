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
    }, 
    watch: {
        modelValue: {
            deep: true,
            handler(){
                this.$emit('assignToDate')
            }
        }
            

    }
}
</script>