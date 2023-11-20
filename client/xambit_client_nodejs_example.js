const axios = require('axios');
const fs = require('fs');

function getFileBuffer(filePath) {
    const fileBuffer = fs.readFileSync(filePath);;
    const result = Array.from(new Uint8Array(fileBuffer));
    return result;
}

function triggerXambitApi(filePath) {
  // Prepare the payload
  const fileBuffer = getFileBuffer(filePath);
  const fileByteArray = Array.from(new Uint8Array(fileBuffer));

  const payload = {
    xapp: {
      xapp: "x-<xapp_id>",
      template: "t-<template_id>",
    },
    collection: "",
    aggregate: true,
    infer: false,
    sandbox: "test",
    hook: {
      url: "https://<some webhook / local proxy URL>.ngrok-free.app", // you'll receive callback here
      method: "POST",
      headers: {
        "test_key": "test_value", // you can set any key-values like credentials here
      },
    },
    file: {
      blob: fileByteArray,
      category: 5, // internal xambit code for bankstatement category
      name: "test_bank_statement.pdf",
    },
  };

  // Send the request
  axios.post("https://<xambit XAPP API URL>/api/predict", payload, {
    headers: {
      "Content-Type": "application/json",
      "x-host": "<host>.xambit.io",
      "x-key": "key-<api key>",
    }
  })
  .then(response => {
    console.log(`Initial response from xAmbit API: ${response.data}`);
  })
  .catch(error => {
    console.log(`Error from xAmbit API: ${error.message}`);
  });
}

// Replace with your actual file path and call the function
const filePath = '<file_path.pdf>';
triggerXambitApi(filePath);
