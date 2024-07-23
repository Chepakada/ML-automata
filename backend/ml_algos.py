import pandas as pd
import numpy as np
import tensorflow as tf
import io

import matplotlib.pyplot as plt
from collections import Counter
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense


COLUMN_NAME = ""

def set_column_name(dependend_column):
    COLUMN_NAME = dependend_column


def distinct_type(content):
    if isinstance(content, str):
        return RNN(content)
    if isinstance(content, pd.DataFrame):
        return Run_tabular(content)



def RNN(content):
    text = content

    vocab = sorted(set(text))
    vocab_size = len(vocab)


    char_to_index = {char: idx for idx, char in enumerate(vocab)}
    index_to_char = np.array(vocab)

   

    # Create a mapping from characters to integers
    char_to_index = {char: idx for idx, char in enumerate(vocab)}
    index_to_char = np.array(vocab)

    # Convert the text to integers
    text_as_int = np.array([char_to_index[char] for char in text])

    # Create training examples and targets
    seq_length = 100  # Increase sequence length for larger inputs
    examples_per_epoch = len(text) - seq_length

    char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

    sequences = char_dataset.batch(seq_length + 1, drop_remainder=True)

    def split_input_target(chunk):
        input_text = chunk[:-1]
        target_text = chunk[1:]
        return input_text, target_text

    dataset = sequences.map(split_input_target)

    # Batch size
    BATCH_SIZE = 64

    # Buffer size to shuffle the dataset
    BUFFER_SIZE = 10000

    dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

    # Build the RNN model
    model = Sequential([
        Embedding(vocab_size, 256, batch_input_shape=[BATCH_SIZE, None]),
        SimpleRNN(1024, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        Dense(vocab_size)
    ])

    # Define the loss function
    def loss(labels, logits):
        return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

    model.compile(optimizer='adam', loss=loss)

    # Train the model
    EPOCHS = 30
    history = model.fit(dataset, epochs=EPOCHS)

    # Function to generate text
    def generate_text(model, start_string, num_generate=500):
        # Convert start string to numbers (vectorize)
        input_eval = [char_to_index[s] for s in start_string]
        input_eval = tf.expand_dims(input_eval, 0)

        # Empty string to store our results
        text_generated = []

        # Temperature controls the randomness of predictions by scaling the logits before applying softmax.
        # Lowering the temperature will result in more predictable text, while increasing it will result in more surprising text.
        temperature = 1.0

        # Reset the model states
        model.reset_states()
        for i in range(num_generate):
            predictions = model(input_eval)
            predictions = tf.squeeze(predictions, 0)

            # Scale the logits by the temperature
            predictions = predictions / temperature
            predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

            # Pass the predicted character as the next input to the model
            # along with the previous hidden state
            input_eval = tf.expand_dims([predicted_id], 0)

            text_generated.append(index_to_char[predicted_id])

        return start_string + ''.join(text_generated)

   
    

    def calculate_perplexity(model, dataset):
        total_loss = 0
        num_batches = 0
        for input_example, target_example in dataset:
            predictions = model(input_example)
            loss = tf.keras.losses.sparse_categorical_crossentropy(target_example, predictions, from_logits=True)
            total_loss += tf.reduce_sum(loss)
            num_batches += 1
        avg_loss = total_loss / num_batches
        perplexity = tf.exp(avg_loss)
        return perplexity
    
    char_freq = Counter(text)

    # Plot character frequency
    plt.figure(figsize=(10, 6))
    plt.bar(char_freq.keys(), char_freq.values())
    plt.xlabel('Characters')
    plt.ylabel('Frequency')
    plt.title('Character Frequency in Text')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    
    
    perplexity = calculate_perplexity(model, dataset)
    return ["RNN", generate_text(model, start_string=COLUMN_NAME, num_generate=500), {"metrix": perplexity}, img]

def Run_tabular( content):
    from sklearn.preprocessing import OneHotEncoder, LabelEncoder
    import seaborn as sns
    df = content
    print("Data accessed")
    if df[COLUMN_NAME].nuniques() < 3 or df[COLUMN_NAME] == "object":
        output = categoric_prediction(df, df[COLUMN_NAME])
    else:
        output = linear_regression(df, df[COLUMN_NAME])

        def scatter_matrix(df):
            sns.pairplot(df)
            plt.suptitle("Scatter Matrix of Features and Target", y = 1.02)

            img = io.BytesIO()
            plt.savefig(img, format = "png")
            img.seek(0)
            plt.close()
            return img
        output.append(scatter_matrix(df))


    def one_hot_encode(df):
        # Identify non-numeric columns
        non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns

        # One-Hot Encode non-numeric columns
        encoder = OneHotEncoder(sparse=False)
        encoded_data = encoder.fit_transform(df[non_numeric_cols])

        # Create a DataFrame with the encoded data
        encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(non_numeric_cols))

        # Drop non-numeric columns and concatenate the encoded DataFrame
        df = df.drop(non_numeric_cols, axis=1)
        df = pd.concat([df, encoded_df], axis=1)
        return df










    def categoric_prediction(df, target_column):
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
        import matplotlib.pyplot as plt
        import seaborn as sns

        
        X = df.drop(columns = [COLUMN_NAME])
        y = target_column
        
        X= one_hot_encode(X)
       

        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

        # Create and train the model
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)


        conf_matrix = confusion_matrix(y_test, y_pred)
        sns.heatmap(conf_matrix, annot = True, cmap = "Blues", fmt = "d", 
                    xticklabels = label_encoder.classes_, 
                    yticklabels=label_encoder.classes_)
        
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.title("Confusion Matrix")

        img = io.BytesIO()
        plt.savefig(img, format = "png" )
        img.seek(0)
        plt.close()

        return ["classification", model, {"accuracy":accuracy, "report":report}, img]







    def linear_regression(df, target_column):

        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        import seaborn

         # Separate the target variable from the features
        
        X = df.drop(columns = [COLUMN_NAME])
        X = one_hot_encode(X)
        y = target_column

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Create and train the linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        def model_efficiency():
            plt.figure(figsize = (10, 6))
            plt.scatter(y_test, y_pred, color = "blue", edgecolors= "k", alpha = 0.7)
            plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--", lw = 3)
            plt.xlabel("Actual")
            plt.ylabel("Predicted")
            plt.title("Actual vs. Predicted Values")

            img = io.BytesIO()
            plt.savefig(img, format = "png")
            img.seek(0)
            plt.close()

            return img

            

        return ["linear_reg", model, {"mae": mae,"mse": mse,"r2":r2}, model_efficiency()]
        
    return output

