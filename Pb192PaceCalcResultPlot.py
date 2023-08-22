import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import sys
import os.path
def get_element(atomic_number):
    elements=["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn", "Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Uut","Fl","Uup","Lv","Uus","Uuo"] 
    return elements[atomic_number-1]

def read_file_list(textFile):
    f=open(textFile,"r")
    file_paths=[]
    inputs=f.readlines()
    for i in inputs:
        file_path=i
        file_path=file_path.replace("/n","")
        file_paths.append(file_path)
    f.close()
    return file_paths
def read_Pace_file(input_file):
    cs4_file=open(input_file)
    i=0
    lines_cs4=cs4_file.readlines()
    products=[]
    for line in lines_cs4:
        product=[]
        if i>=2:
            linesplit=line.split()
            proton_n=linesplit[0]
            neutron_n=linesplit[1]
            crossection=linesplit[2]
            proton_n=int(proton_n)
            neutron_n=int(neutron_n)
            crossection=float(crossection)
            massnumber=proton_n+neutron_n
            product.append(proton_n)
            product.append(massnumber)
            product.append(crossection)
            products.append(product)

        if i==1:
            linesplit=line.split(" ")
            compound_energy=linesplit[3]
        i=i+1

    #read html file
    html_text=input_file.replace(".cs4",".html")
    htmlfile=open(html_text)
    line_html=htmlfile.readlines()
    linesplit=line_html[0].split("Bombarding energy (MeV)</em></td><td> ")
    linesplit=linesplit[1].split( "</td></tr><tr><td><em> Center of mass energy")
    energy=linesplit[0]
    linesplit=line_html[0].split("Total fission</b>   </td><td></td><td align=center>")
    linesplit=linesplit[1].split("</td></tr><tr style=\"color:green\"><td colspan=2>  <b>TOTAL </b>")
    fission_events,fission_presentage,fission_crossection=linesplit[0].split("</td><td align=center>")
    linesplit=line_html[0].split("Projectile</em></td><td align=center>")
    linesplit=linesplit[1].split("</td><td align=center>0</td></tr><tr><td><em>Target")
    print(linesplit[0].split("</td><td align=center>"))
    projectile_z,projectile_n,projectile_A=linesplit[0].split("</td><td align=center>")
    linesplit=line_html[0].split("Target</em></td><td align=center>")
    linesplit=linesplit[1].split("</td><td align=center>0</td></tr><tr><td><em>Compound nucleus")
    target_z,target_n,target_A=linesplit[0].split("</td><td align=center>")

    fission_crossection=fission_crossection.replace(" ","")
    energy=energy.replace(" ","")
    print(fission_events)
    print(fission_presentage)
    print(fission_crossection)
    print(energy)
    beam=[projectile_z,projectile_A]
    target=[target_z,target_A]
    print(beam)
    print(target)
    print(compound_energy)
    print(products)
    cs4_file.close()
    htmlfile.close()
    return energy,target,beam,compound_energy,fission_crossection,products

def write_file(energy, target, beam, com_energy,fission,products,output_file):
    file=open(output_file,"a")
    element_target=get_element(int(target[0]))
    element_beam=get_element(int(beam[0]))
    file.write("Target:"+target[1]+element_target+"\n")
    file.write("Beam:"+beam[1]+element_beam+" Energy:"+str(energy)+" Compound_Energy:"+str(com_energy)+"\n")
    file.write("Product"+" Cross-section"+"\n")
    for product in products:
        element_product=get_element(product[0])
        file.write(str(product[1])+element_product+" "+str(product[2])+"\n")
    file.write("Fission cross-section:"+str(fission)+"\n")

def search_product(energies,products_all):
    products_all_sorted=[]
    firstTime=0

    for i in range(len(products_all)):
        energy=energies[i]
        products=products_all[i]
        print(products)
        print(energy)
        #input("Here are energies and products:Press Enter to continue...")
        for j in range(len(products)):
            Z=products[j][0]
            A=products[j][1]
            cross_section=products[j][2]
            crossectionsorted=[cross_section]
            energysorted=[energy]
            if (firstTime==0):
                product_sorted=[Z,A,energysorted,crossectionsorted]
                products_all_sorted.append(product_sorted)
                firstTime=1
                print(products_all_sorted)
               # input("HereFirstTime:Press Enter to continue...")
            else:
                did_we_found=0
                for i in range(len(products_all_sorted)):
                    if products_all_sorted[i][0]==Z:
                        if products_all_sorted[i][1]==A:
                            print(products_all_sorted[i])
                            print(products_all_sorted[i][2])
                            energysorted=products_all_sorted[i][2]
                            energysorted.append(energy)
                            products_all_sorted[i][2]=energysorted
                            crossectionsorted=products_all_sorted[i][3]
                            crossectionsorted.append(cross_section)
                            products_all_sorted[i][3]=crossectionsorted
                            print(products_all_sorted[i])
                            did_we_found=1
                            print(products_all_sorted)
                            #input("HereSecondTimePress Enter to continue...")
                            break
                if did_we_found==0:
                    
                    product_sorted=[Z,A,energysorted,crossectionsorted]
                    products_all_sorted.append(product_sorted)
                    print(products_all_sorted)
                    #input("Press Enter to continue...")
    return products_all_sorted


            


#Initialise the plot, size of the figure. 
def intialise_plot(plt):
    xmin=330
    xmax=390
    ymin=-30
    ymax=400
    xTitle=r"Beam energy [MeV]"
    yTitle=r"Cross-section [mb]"
    fontSize=20
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["figure.figsize"] = (11.5,7.5)
    plt.rc('text', usetex=True)
   # plt.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
    return xmin,xmax,ymin,ymax,xTitle,yTitle,fontSize
def plotCrosSection(energies,target,beam,fissions,products_sorted,name_of_figure):
    x_min,x_max,y_min,y_max,xTitle,yTitle,fontSize=intialise_plot(plt)
    fig, ax = plt.subplots()
    plt.ylim(y_min,y_max)
    plt.xlim(x_min,x_max)
    minor_locator = AutoMinorLocator(5)
    ax.yaxis.set_minor_locator(minor_locator)
    ax.tick_params(which="major",direction="in",length=8,labelsize=fontSize)
    ax.tick_params(which="minor",direction="in",length=4,labelsize=fontSize)
    minor_locatorx = AutoMinorLocator(5)
    ax.xaxis.set_minor_locator(minor_locatorx)
    ax.tick_params(which="major",direction="in",length=8,labelsize=fontSize)
    ax.tick_params(which="minor",direction="in",length=4,labelsize=fontSize)
    plt.xlabel(xTitle,fontsize=fontSize)
    plt.ylabel(yTitle,fontsize=fontSize)
    print(target[0])
    element_target=get_element(int(target[0]))
    element_beam=get_element(int(beam[0]))
    plt.title(r"$^{{{0}}}${1}+$^{{{2}}}${3}".format(target[1],element_target,beam[1],element_beam),fontsize=fontSize)
    plt.plot(energies,fissions,color='green',linestyle='dashed',label="Fission")
    for product in products_sorted:
        element_product=get_element(product[0])
        print("Plotting")
        print(product[2])
        print(product[3])
        if product[0]==82:
            plt.plot(product[2],product[3],marker="o",linestyle='solid',label=r"{1}-{0}".format(str(product[1]),element_product))
        elif product[0]==81:
            plt.plot(product[2],product[3],marker="X",linestyle='solid',label=r"{1}-{0}".format(str(product[1]),element_product))
        elif product[0]==80:
             plt.plot(product[2],product[3],marker="s",linestyle='solid',label=r"{1}-{0}".format(str(product[1]),element_product))
    legend = ax.legend(ncol=5,loc='upper left', shadow=True, fontsize=fontSize-5)
   
    plt.savefig(name_of_figure,format="pdf", bbox_inches="tight")
    plt.show()


in_file_name=sys.argv[1]
output_file="Pb-192_110Pd_86Kr.txt"
name_of_figure="Pb-192_110Pd_86Kr.pdf"
file_path_list=read_file_list(in_file_name)
energies=[]
fissions=[]
products_all=[]
for i in file_path_list:
    i=i.replace("\n","")
    energy, target, beam, com_energy,fission,products=read_Pace_file(i)
    write_file(energy, target, beam, com_energy,fission,products,output_file)
    energies.append(float(energy))
    fissions.append(float(fission))
    products_all.append(products)
products_sorted=search_product(energies,products_all)
plotCrosSection(energies,target,beam,fissions,products_sorted,name_of_figure)
        