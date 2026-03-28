FROM node:18

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy application source
COPY . .

EXPOSE 3000

CMD ["npm", "start"]
