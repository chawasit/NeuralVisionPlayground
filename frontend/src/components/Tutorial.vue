<template>
  <b-container>
    <h1>Tutorial</h1>
    <div class="float-right sticky-top pt-4">
      <b-list-group v-b-scrollspy>
        <b-list-group-item href="#MNIST">MNIST Dataset</b-list-group-item>
        <b-list-group-item href="#neural_network">What is Neural network</b-list-group-item>
        <b-list-group-item href="#gd">Gradient Descend</b-list-group-item>
        <b-list-group-item href="#convolution">Image Filtering and Convolution</b-list-group-item>
        <b-list-group-item href="#cnn">Convolution Neural Network</b-list-group-item>
        <b-list-group-item href="#compo_cnn">Component of CNN</b-list-group-item>
        <b-list-group-item href="#pooling">Pooling Layer</b-list-group-item>
        <b-list-group-item href="#softmax">Softmax Layer</b-list-group-item>
        <b-list-group-item href="#overfit">Over-fitting</b-list-group-item>
        <b-list-group-item href="#dropout">Dropout</b-list-group-item>
      </b-list-group>
    </div>
    <b-row>
      <b-col cols="10">
        <div class="pt-2">
          <div class="mb-5">
            <h4 id="MNIST">MNIST Dataset</h4>
            <p>
              MNIST dataset เป็นชุดข้อมูลของ รูปภาพตัวเลข 0 ถึง 9 ที่เขียนด้วยมือในรูปแบบต่างๆ ที่ถูกเตรียมไว้ให้เหมาะสมกับการนำมาใช้ในการทำ machine learing
            </p>
            <img src="../assets/mnist.png" alt="MNIST Dataset" class="img-fluid mx-auto d-block" width="600">
            <p>
              ข้อมูลของ MNIST Dataset แต่ละตัว จะเป็นไฟล์รูปภาพขาว-ดำขนาด 28 x 28 พิกเซล ซึ่งสามารถแปลงรูปดังกล่าว ให้เป็นชุดของตัวเลขขนาด 28 x 28 = 784 ตัว เพื่อนำมาประมวลผลต่อได้
            </p>
            <img src="../assets/mnist_sample.png" alt="mnist sample" class=" img-fluid mx-auto d-block" width="600">
          </div>
          <div class="mb-5">
            <h4 id="neural_network">What is Neural Network</h4>
            <p>
              &emsp;Neural network เป็นวิธีการสำหรับสร้างโปรแกรมคอมพิวเตอร์ที่เรียนรู้จากข้อมูล มีแนวคิดมาจากเส้นประสาทของคนว่าสมองคนนั้นทำงานอย่างไร โดยจะมีโมเดลที่ถูกคำนวณมาแล้วเพื่อให้สามารถทำงานได้คล้ายกับสมองของคน แต่ละตัวจะเชื่อมต่อกันเป็นชั้นๆและแต่ละตัวจะรับข้อมูลเข้าไป เช่น รูปภาพ แล้วนำข้อมูลที่รับมามาคำนวณทำอะไรสักอย่าง หลังจากนั้นจะส่งข้อมูลที่คำนวณเสร็จแล้วไปที่ตัวต่อไป
            </p>
            <img src="../assets/hidden_layer.png" alt="Hidden Layer" class=" img-fluid mx-auto d-block" width="600">
            <p>
              การจะทำแบบนี้ได้ ขั้นแรกเราต้องสอนให้คอมพิวเตอร์รู้จักก่อนว่ารูปแต่ละรูปคือรูปอะไร เช่น รูปแมว รูปรถ รูปหนังสือ ในที่นี้เราใช้รูปตัวเลขจาก MNIST dataset ยิ่งคอมพิวเตอร์เห็นรูปมากเท่าไหร่ ความสามารถในการจำแนกก็ยิ่งมากขึ้น
            </p>
            <br>
            <img src="../assets/class_labels.png" alt="Class labels" class=" img-fluid mx-auto d-block" width="600">
            <p>
              การทำแบบนี้เรียกว่า Supervised learning คอมพิวเตอร์จะเริ่มจดจำรูปแบบของตัวเลขในแต่ละรูปที่ไม่มีในรูปอื่นและเริ่มการเรียนรู้ของตัวมันเอง
            </p>
          </div>
          <div class="mb-5">
            <h4 id="gd">Gradient Descend</h4>
            <p>
              อัลกอริทีมที่ใช้หาจุดต่ำสุดหรือสูงสุดของฟังค์ชั่นOptimization คือการหาจุดที่เหมาะสมที่สุด (Optimal Point) สำหรับปัญหาใดปัญหาหนึ่ง หนึ่งใน Algorithm สำหรับการทำ Optimization ตัวนึงที่ชื่อว่า Gradient Descent ซึ่งเป็น Algorithm ที่ใช้ค่อนข้างบ่อยในเรื่อง Machine Learning 
            </p>
            <p>
              หากเราเปรียบเทียบ Gradient Descent กับการปีนเขา ให้ลองนึกดูว่า เรากำลังยืนอยู่บนยอดเขา แล้วต้องการจะลงไปที่บ่อน้ำที่อยู่ในจุดต่ำที่สุดของเขา แต่เรามองไม่เห็นว่าไอบ่อน้ำเนี่ย มันต้องเดินไปทางไหน มันอยู่ตรงไหนจากจุดที่เรายืนอยู่ หนำซ้ำความไม่เท่ากันของสันเขาที่บดบังการมองเห็น ทำให้เรามองไม่เห็นว่าไปทางไหนถึงจะลงไปถึงจุดต่ำสุดได้ สิ่งที่เราจะทำได้ก็คือ มองไปรอบ ๆ แล้ว พิจารณาหาจุดต่ำสุดเท่าที่เห็น แล้วเลือกเดินไปทางนั้นเรื่อย ๆ จนถึงบ่อน้ำในที่สุด
            </p>
            <p>
              หากเรามองเป็นภาพสามมิติ ก็จะเป็นเหมือนกราฟด้านล่างนี้
            </p>
              <img src="../assets/error_plane.png" alt="Gradient descend" class=" img-fluid mx-auto d-block" width="600">
            <p>
              จากภาพ พื้นที่สีแดงคือยอดเขา (สูงมาก) และสีน้ำเงินคือบ่อน้ำ (ต่ำมาก) จะเห็นว่า หากเรายืนอยู่คนละจุดกัน ก็จะทำให้เราไปเจอบ่อน้ำคนละบ่อกัน ซึ่งบ่อน้ำเราเรียกว่า local minima ส่วนบ่อน้ำที่ต่ำที่สุดในโจทย์ของเราคือ global minima 
            </p>
            <p>
              สำหรับ Neural Network เราจำเป็นต้องหา gradient เพื่อใช้ในอัลกอรึทึมที่เรียกว่า back propagation เพื่อหาพารามิเตอร์ของ Neural Network
            </p>
          </div>
          <div class="mb-5">
            <h4 id="convolution">Image Filtering and Convolution</h4>
            <p>
              convolution เป็น 1 ในขั้นตอนที่สำคัญที่สุดในการใช้ signal และ การทำ processing ต่างๆ โดยสามารถใช้ในการทำ 1D (ยกตัวอย่างเช่น speech processing) , 2D (ยกตัวอย่างเช่น image processing) or 3D (ยกตัวอย่างเช่น video processing) ซึ่งการ convolution ส่วนมากใช้ใน image processing เพื่อดึงเอา feature กับ core ของ Convolution Neural Networks (CNNs) มาใช้
            </p>
            <p>
              เราสามารถพิจารณาภาพโดยใช้ matrix ที่ใช้ตัวเลขระหว่าง 0 – 255 ขนาดของ matrix จะหาได้จาก (ความสูง) x (ความกว้าง) x (จำนวนของ channels) ซึ่งใน 1 ภาพโทนขาวดำจะมี 1 channel ในขณะที่ ภาพสีจะมีถึง 3 channels (RGB)
            </p>
            <img src="../assets/sample_img1.jpg" alt="Sample image1" class=" img-fluid mx-auto d-block" width="600">
            <p>
              ถ้าเราขยายภาพไปยังบริเวณส่วนหนึ่งของภาพ เราสามาถเห็น pixels ของรูปภาพได้ และสามารถนำมาทำเป็นค่าตัวเลขได้เหมือนในภาพด้านล่าง
            </p>
            <img src="../assets/sample_img2.jpg" alt="Sample image2" class=" img-fluid mx-auto d-block" width="600">
          </div>
          <div class="mb-5">
            <h4 id="cnn">Convolution Neural Network</h4>
            <p>
              เป็นเทคนิคที่นิยมใข้กันมากในการเพิ่มความแม่นยำให้กับการจำแนกรูปภาพ โดย CNN จะทำงานเหมือน Neural Network ทั่วไปเพียงแต่ว่าจะมี convolution layer เพิื่มมาในตอนแรก
            </p>
            <p>
              จากที่เราจะใส่รูปเข้าไปทั้งรูป (โดยเป็นชุดข้อมูลตัวเลข) เราจะแบ่งรูปออกเป็นรูปย่อยๆ คอมพิวเตอร์จะพยายามคาดเดาแต่ละรูปย่อย การทำแบบนี้ทำให้คอมพิวเตอร์สามารถประมวลผลพร้อมกันและตรวจหาตัวเลข (Object) ว่าอยู่ตรงไหน
            </p>
            <img src="../assets/cnn.png" alt="CNN" class=" img-fluid mx-auto d-block" width="600">
          </div>
          <div class="mb-5">
            <h4 id="compo_cnn">Component of Convolution Neural Network</h4>
            <div class="mb-4">
              <h5 id="pooling">Pooling Layer</h5>
              <p>
                Pooling layer คือชั้นที่ทำการลดขนาดของข้อมูล ด้วยการทำการดึงข้อมูลตัวแทนของข้อมูลภายใต้ kernal size เดียวกัน โดยรูปแบบของการ pooling มี สองแบบ คือ
              </p>
              <p>
                <ul>
                  <li>Max pooling<br></li>
                  คือการดึงค่าที่มากที่สุดของ แต่ละ kernel (สีแต่ละสีแสดงถึงแต่ละ kernel) มาเป็นตัวแทน
                </ul>
              </p>
              <p>
                <ul>
                    <li>Average pool<br></li>
                    คือการดึงค่าเฉลี่ยของ แต่ละ kernel (สีแต่ละสีแสดงถึงแต่ละ kernel) มาเป็นตัวแทน
                </ul>
              </p>
              <img src="../assets/pooling.png" alt="Pooling" class=" img-fluid mx-auto d-block" width="600">
            </div>
            <div>
              <h5 id="softmax">Softmax Layer</h5>
              <img src="../assets/softmax_eq.png" alt="Softmax Equation" class=" img-fluid mx-auto d-block">
              <p>
                เป็น layers ชั้นสุดท้าย ที่มีหน้าที่ในการประเมินผลลัพธ์ที่ออกมาจากการทำงาน ให้อยู่ในรูปของความน่าจะเป็นของแต่ละผลลัพธ์ เพื่อให้สามารถสามารถวิเคราะห์ผลลัพธ์ และความสัมพันธ์ของแต่ละความเป็นไปได้ของคำตอบได้
              </p>
            </div>
          </div>
          <div class="mb-5">
            <h4 id="overfit">Over-fitting</h4>
            <p>
              เป็นอีกหนึ่งปัญหาพื้นฐานที่พบบ่อยมากในการพัฒนาอัลกอรึทิ่ม Machine Learning ทำให้เกิดเหตุการณ์ที่ โมเดลทำงานได้ดีมากกับข้อมูลตัวอย่างที่เราใช้ฝึกแต่เมื่อไหร่ก็ตามที่เรานำโมเดลนั้นมาทำงานกันกับข้อมูลที่โมเดลไม่เคยเห็นมาก่อน จะทำงานได้แย่มาก
            </p>
            <p>
              การแก้ไขปัญหา Over-fitting คือการลดจำนวน พารามิเตอร์ที่สามารถปรับค่าได้ให้เหลือน้อยลงเพื่อสร้างตัวทำนายที่เหมาะสมกับข้อมูล
            </p>
            <img src="../assets/overfit.png" alt="Overfitting comparison">
          </div>
          <div class="mb-5">
            <h4 id="dropout">Dropout</h4>
            <p>
              คือการสุ่มทิ้ง node บางตัวออกไปจาก neural network โดย node ที่เราทิ้งไปแล้วจะไม่ถูกนำไปรวมในการคำนวนใดเลย ซึ่งไอเดียที่ทิ้ง node ไปนั้นก็เพื่อแก้ไขปัญหา over-fitting จากการที่มีจำนวน node มากเกินไปจนทำให้ตัวโมเดลมีความซับซ้อนมากเกินความจำเป็น
            </p>
            <img src="../assets/dropout.png" alt="Dropout" class=" img-fluid mx-auto d-block" width="600">
            <img src="../assets/droput_graph.png" alt="Overfit graph" class=" img-fluid mx-auto d-block" width="600">
            <p>
              การ dropout จึงถือเป็นขั้นตอนที่สำคัญขั้นตอนหนึ่ง ซึ่งจะลดการเกิด overfitting จะส่งผลให้สามารถทำการทำนายผลมีประสิทธิภาพที่ดีขึ้นอีกด้วย
            </p>
          </div>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'Tutorial'
}
</script>
