// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCXOKzOkQHGh1yJ8BDrIwibm8HZK8i91vY",
  authDomain: "satfussion.firebaseapp.com",
  projectId: "satfussion",
  storageBucket: "satfussion.firebasestorage.app",
  messagingSenderId: "419400121975",
  appId: "1:419400121975:web:66226e2257cbd8f0acd072",
  measurementId: "G-WBV43LCQZF"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);