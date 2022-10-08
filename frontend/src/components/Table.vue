<template>
    <table class="table">
        <thead>
            <TableRowHeader
            />
        </thead>
        <tbody>
            <TableRowBody
            />
        </tbody>
    </table>
</template>
<script>
import TableRowHeader from "./TableRowHeader.vue"
import TableRowBody from "./TableRowBody.vue"
export default {
    name: "Table",
    components:{
        TableRowHeader,
        TableRowBody,
    },
}
</script>
<style>
    .table {
        margin: auto;
        width: 350px;
    }
    .table td {
        height:40px;
    }
</style>
