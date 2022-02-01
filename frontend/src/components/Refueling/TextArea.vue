<template>
    <textarea v-model="text" class="form-control" style="height:80px;"></textarea>
</template>
<script>

export default {
    name: "TextArea",
    props:{
        text: "",
    },
    computed:{
        text: {
            get(){
                return ""
            },
            set(val){
                this.$emit("typed", val)
            }
        }
    }
}
</script>