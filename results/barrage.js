import http from 'k6/http';
import { sleep } from 'k6';

let params = {
  timeout: '120s'
};

export default function () {
    http.get(__ENV.URL, params);
    sleep(0.1);
}