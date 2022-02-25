<template>
    <tr >
        <td v-for="data in datas" :key="data">
            {{data}}
        </td>
    </tr>
</template>
<script>
export default {
    name: "TableRowBody",
    props: ["datas"],
}
</script>