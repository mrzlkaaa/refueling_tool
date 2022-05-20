<template>
    <textarea v-model="text" class="form-control" style="height:80px;"></textarea>
</template>
<script>

export default {
    name: "TextArea",
    props:["modelValue"],
    computed:{
        text: {
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