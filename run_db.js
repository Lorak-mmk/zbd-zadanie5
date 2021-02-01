const express = require("express");
const { postgraphile } = require("postgraphile");
const ConnectionFilterPlugin = require("postgraphile-plugin-connection-filter");

const app = express();

app.use(
  postgraphile(process.env.DATABASE_URL, "public", {
    appendPlugins: [ConnectionFilterPlugin],
    graphiql: true,
    watchPg: true,
    enhanceGraphiql: true,
    dynamicJson: true,
    setofFunctionsContainNulls: false,
    showErrorStack: "json",
    extendedErrors: ["hint", "detail", "errcode"],
    exportGqlSchemaPath: "schema.graphql",
    enableQueryBatching: true,
    graphileBuildOptions: {
        connectionFilterRelations: true, // default: false
        connectionFilterAllowEmptyObjectInput: true, // default: false
        connectionFilterAllowNullInput: true, // default: false
        connectionFilterAllowedOperators: [
            "equalTo",
            "lessThanOrEqualTo",
            "greaterThanOrEqualTo",
        ],
    },
  })
);

app.listen(5000);
