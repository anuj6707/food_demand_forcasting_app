from flask import Flask,redirect,render_template,url_for,request
import pandas as pd
import pickle

app=Flask(__name__)
filename="model.pkl"
with open(filename, "rb") as f:
   predmodel = pickle.load(f)

@app.route('/',methods=["GET",'POST'])
def home():
    if request.method=="GET":
      return render_template("home.html")

@app.route('/prediction',methods=["GET",'POST'])
def prediction():
   if request.method=="GET":
      return render_template("prediction.html")
   else:
      try:
         week=int(request.form['week'])
         center_id=str(request.form['center_id'])
         meal_id=str(request.form['meal_id'])
         checkout_price=float(request.form['checkout_price'])
         base_price=float(request.form['base_price'])
         emailer_for_promotion=int(request.form['emailer_for_promotion'])
         homepage_featured=int(request.form['homepage_featured'])
         df12 = pd.DataFrame({
    "week": [week],
    "center_id": [center_id],
    "meal_id": [meal_id],
    "checkout_price": [checkout_price],
    "base_price": [base_price],
    "emailer_for_promotion": [emailer_for_promotion],
    "homepage_featured": [homepage_featured]
})
         df12["discount"] = (df12["base_price"] - df12["checkout_price"]) / df12["base_price"]

         df12["promo_discount"] = (df12["discount"]* df12["homepage_featured"]* df12["emailer_for_promotion"])
         df12 = pd.get_dummies(df12,columns=["meal_id", "center_id"])
         feature_columns=['week', 'checkout_price', 'base_price', 'emailer_for_promotion', 'homepage_featured', 'discount', 'meal_id_1062', 'meal_id_1109', 'meal_id_1198', 'meal_id_1207', 'meal_id_1216', 'meal_id_1230', 'meal_id_1247', 'meal_id_1248', 'meal_id_1311', 'meal_id_1438', 'meal_id_1445', 'meal_id_1525', 'meal_id_1543', 'meal_id_1558', 'meal_id_1571', 'meal_id_1727', 'meal_id_1754', 'meal_id_1770', 'meal_id_1778', 'meal_id_1803', 'meal_id_1847', 'meal_id_1878', 'meal_id_1885', 'meal_id_1902', 'meal_id_1962', 'meal_id_1971', 'meal_id_1993', 'meal_id_2104', 'meal_id_2126', 'meal_id_2139', 'meal_id_2290', 'meal_id_2304', 'meal_id_2306', 'meal_id_2322', 'meal_id_2444', 'meal_id_2490', 'meal_id_2492', 'meal_id_2494', 'meal_id_2539', 'meal_id_2569', 'meal_id_2577', 'meal_id_2581', 'meal_id_2631', 'meal_id_2640', 'meal_id_2664', 'meal_id_2704', 'meal_id_2707', 'meal_id_2760', 'meal_id_2826', 'meal_id_2867', 'meal_id_2956', 'center_id_10', 'center_id_11', 'center_id_13', 'center_id_14', 'center_id_17', 'center_id_20', 'center_id_23', 'center_id_24', 'center_id_26', 'center_id_27', 'center_id_29', 'center_id_30', 'center_id_32', 'center_id_34', 'center_id_36', 'center_id_39', 'center_id_41', 'center_id_42', 'center_id_43', 'center_id_50', 'center_id_51', 'center_id_52', 'center_id_53', 'center_id_55', 'center_id_57', 'center_id_58', 'center_id_59', 'center_id_61', 'center_id_64', 'center_id_65', 'center_id_66', 'center_id_67', 'center_id_68', 'center_id_72', 'center_id_73', 'center_id_74', 'center_id_75', 'center_id_76', 'center_id_77', 'center_id_80', 'center_id_81', 'center_id_83', 'center_id_86', 'center_id_88', 'center_id_89', 'center_id_91', 'center_id_92', 'center_id_93', 'center_id_94', 'center_id_97', 'center_id_99', 'center_id_101', 'center_id_102', 'center_id_104', 'center_id_106', 'center_id_108', 'center_id_109', 'center_id_110', 'center_id_113', 'center_id_124', 'center_id_126', 'center_id_129', 'center_id_132', 'center_id_137', 'center_id_139', 'center_id_143', 'center_id_145', 'center_id_146', 'center_id_149', 'center_id_152', 'center_id_153', 'center_id_157', 'center_id_161', 'center_id_162', 'center_id_174', 'center_id_177', 'center_id_186', 'promo_discount']
         df12 = df12.reindex(columns=feature_columns, fill_value=0)
         if f"center_id_{center_id}" not in feature_columns:
                return render_template("prediction.html",error="Invalid Center ID. Please enter a valid center.")

         if f"meal_id_{meal_id}" not in feature_columns:
                return render_template("prediction.html",error="Invalid Meal ID. Please enter a valid meal.")
         prediction=int(predmodel.predict(df12)[0])
         if prediction<0:
            prediction=0
         else :
            prediction=prediction
         return render_template("prediction.html",prediction=prediction)
      except Exception:

        return render_template("prediction.html",error="Something went wrong while generating the prediction.")
   
@app.route('/insights',methods=["GET",'POST'])
def insight():
   if request.method=="GET":
      
      

      
      return render_template("insights.html",)
   




if __name__=="__main__":
    app.run(debug='False')


