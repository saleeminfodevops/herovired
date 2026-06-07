
AWS Deployment architecture diagram. 

<img width="821" height="611" alt="TravelMemory-Drawing" src="https://github.com/user-attachments/assets/89273202-9dd2-4ef7-8d48-a41b4d8579f3" />

1) 2 Instances in ap-south-1
<img width="830" height="152" alt="1-instances" src="https://github.com/user-attachments/assets/931f489f-7516-44fb-b6f9-86247a4292b9" />

2) Created Security Group
<img width="805" height="961" alt="2-sg-rules" src="https://github.com/user-attachments/assets/4f597709-ea34-4534-9269-94e0dca67d8f" />

3) Installed and configured nginx for reverse proxy
<img width="1726" height="934" alt="3-nginx" src="https://github.com/user-attachments/assets/6f6f9199-2832-4922-adb9-5289b778dc16" />

5) Clone the TravelMemory repo
<img width="1202" height="321" alt="4-clone-travelMemory" src="https://github.com/user-attachments/assets/b3d3da36-60f8-4e34-ba7d-fd2bde722aa5" />

6) Created and edited the Docker config files
<img width="1243" height="442" alt="5-docker-files" src="https://github.com/user-attachments/assets/866658b1-29e6-4fbb-8740-0d73f08667d9" />
<img width="1843" height="688" alt="6-docker-build-run" src="https://github.com/user-attachments/assets/1bc47232-8edc-4540-8b1e-3f7804186f48" />


7) Build and run the TravelMemory project
<img width="1843" height="688" alt="6-docker-build-run" src="https://github.com/user-attachments/assets/af686bbe-9afe-40bd-8444-eafcf8acdb96" />

8) Created an ApplicationLoadBalance and HostHeader Rule
<img width="1694" height="655" alt="7a-aws-lb-rule" src="https://github.com/user-attachments/assets/809c61df-ceff-4c94-b19e-22236e1c8dc5" />

<img width="1695" height="746" alt="7-aws-lb" src="https://github.com/user-attachments/assets/05708e13-52a7-4a06-9d48-a5c9f22512ee" />


8) Registered Domain and Created a CNAME Record
<img width="1422" height="689" alt="8-cloudflare-cname" src="https://github.com/user-attachments/assets/4650bdab-9a38-4f31-af82-9b92a5e6b9cf" />












