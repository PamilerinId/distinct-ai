// file-upload.service.js

import * as axios from 'axios';

const BASE_URL = 'http://localhost:5000';

function upload(formData) {
  axios({
    url: BASE_URL,
    method: 'GET',
    responseType: 'blob', // important
  }).then((response) => {
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'file.pdf');
    document.body.appendChild(link);
    link.click();
  });
}

export default upload;
